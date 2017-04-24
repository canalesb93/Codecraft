# -----------------------------------------------------------------------------
# parser.py
#
# Utilizes lexer for parsing BNF rules
# -----------------------------------------------------------------------------

import sys
from libraries.ply import lex
from libraries.ply import yacc

# Classes

import scanner
from enumerators import *
from classes import *
from cube import *
from operations import *
from memory import MemorySystem

if sys.version_info[0] >= 3:
    raw_input = input

# =============== Lexer SETUP ===============
tokens = scanner.tokens
lex.lex(module=scanner)

# =============== Global START ===============

'''
Prepend "__" to all global variables for easy undestanding.
Remember to use "global" when modifying these variables in 
a different scope.
''' 

# Quadruple Setup
__quadruples = QuadrupleList()
__operandStack = Stack()
__operationStack = Stack()
__typeStack = Stack()
__jumpStack = Stack()

# Symbol Tables
__constantTable = SymbolTable() # { 'address':counter, 'type':Type, 'val':value }
__varsGlobal = SymbolTable()
__varsLocal = SymbolTable()
__funcsGlobal = FunctionTable()

# Temporary Var/Func data
# Vars
__tVarType = None
__tVarName = None
__tVarIsArray = False
# Funcs
__tFuncName = None
__tFuncType = None
__tFuncParameters = []
# Func Calls
__tCallName = None
__tCallType = None
__tCallArgCount = 0

# Scope
__scope = Scope.GLOBAL
__memory = MemorySystem()

def setLocalScope():
  global __scope 
  __scope = Scope.LOCAL

def setGlobalScope():
  global __scope 
  __scope = Scope.GLOBAL

# =============== Global END ===============

# =============== Grammar START ===============

def p_program(p):
  'program : CRAFT "{" canvas_block "}"'

def p_canvas_block(p):
  '''canvas_block : block canvas_block
                  | function canvas_block
                  | empty'''

def p_type(p):
    '''type : VOID
            | INT
            | FLOAT
            | CHAR
            | BOOL
            | STRING'''
    if(p[1] == 'void'):
      p[0] = Type.VOID
    elif(p[1] == 'int'):
      p[0] = Type.INT
    elif(p[1] == 'float'):
      p[0] = Type.FLOAT
    elif(p[1] == 'char'):
      p[0] = Type.CHAR
    elif(p[1] == 'bool'):
      p[0] = Type.BOOL
    elif(p[1] == 'string'):
      p[0] = Type.STRING

# ===== VARIABLES =====

def p_vars(p):
    '''vars : VAR type saveVariableType var'''

def p_var(p):
    '''var : ID addVariable var_array var_assignment var_repeater
           '''

def p_var_repeater(p):
    '''var_repeater : "," var
                    | empty
                    '''

def p_var_assignment(p):
    '''var_assignment : pushIdOperand "=" pushOperation super_expression addAssignmentQuadruple
                      | empty
                      '''

def p_var_array(p):
    '''var_array : "[" CTE_INT "]" setTypeAsArray
                 | empty'''

# def p_assignment_array(p):
#     '''assignment_array : ID "=" "{" parameters "}" ',' assignment
#                         | ID "=" "{" parameters "}" 
#                         | ID
#                         '''
#     pass

def p_var_free_assignment(p):
    '''var_free_assignment : ID lookupId var_assignment'''

# ===== FUNCTIONS =====

def p_function(p):
    ''' function : FUNCTION setLocalScope type saveFunctionType ID saveFunctionName "(" parameters_definition ")" addFunction "{" block_repeater "}" endFunction setGlobalScope
                 ''' 

def p_parameters_definition(p):
    '''parameters_definition : type saveVariableType ID addParameter parameters_definition1
                             | empty''' 

def p_parameters_definition1(p):
    '''parameters_definition1 : "," type saveVariableType ID addParameter parameters_definition1
                              | empty'''

def p_parameters(p):
    '''parameters : super_expression addArgument parameters1
                  | empty'''

def p_parameters1(p):
    '''parameters1 : "," super_expression addArgument parameters1
                   | empty'''

# pending: return on void and when free roaming the return
def p_return(p):
    '''return : RETURN
              | RETURN super_expression returnFunctionValue'''

def p_function_call(p):
    '''function_call : ID "(" lookupFunction startFunctionCall parameters ")" verifyArguments endFunctionCall checkForReturn
                     | ID "(" lookupFunction ")" endFunctionCall checkForReturn'''

def p_block_repeater(p):
    '''block_repeater : block block_repeater
                      | empty'''

def p_block(p):
    '''block : vars
             | var_free_assignment
             | if
             | cycle
             | return
             | BREAK
             | CONTINUE
             | function_call'''

# ===== CONDITIONALS =====

def p_if(p):
    '''if : IF "(" super_expression ")" ifConditional "{" block_repeater "}" endIfConditional
          | IF "(" super_expression ")" ifConditional "{" block_repeater "}" else'''

def p_else(p):
    '''else : ELSE elseConditional else_if
            | ELSE "{" elseConditional block_repeater "}" endIfConditional'''

def p_else_if(p):
    '''else_if : IF "(" super_expression ")" ifConditional "{" block_repeater "}" endElseIfConditional 
               | IF "(" super_expression ")" ifConditional "{" block_repeater "}" else_if_else'''

def p_else_if_else(p):
    '''else_if_else : ELSE elseIfConditional else_if
                    | ELSE "{" elseIfConditional block_repeater "}" endIfConditional'''

def p_cycle(p):
    'cycle : WHILE startLoop "(" super_expression ")" loopConditional "{" block_repeater "}" endLoop'

# ===== EXPRESSIONS =====

def p_super_expression(p):
  '''super_expression : expression tryLogicalQuadruple
                      | expression tryLogicalQuadruple AND pushOperation super_expression
                      | expression tryLogicalQuadruple OR pushOperation super_expression'''

def p_expression(p):
  '''expression : exp tryRelationalQuadruple
                | exp tryRelationalQuadruple '>' pushOperation expression
                | exp tryRelationalQuadruple '<' pushOperation expression
                | exp tryRelationalQuadruple EQ pushOperation expression
                | exp tryRelationalQuadruple LESS_EQ pushOperation expression
                | exp tryRelationalQuadruple GREATER_EQ pushOperation expression'''

def p_exp(p):
  '''exp : term tryAddSubQuadruple
         | term tryAddSubQuadruple '+' pushOperation exp
         | term tryAddSubQuadruple '-' pushOperation exp '''

def p_term(p):
  '''term : factor tryMultDivQuadruple
          | factor tryMultDivQuadruple '*' pushOperation term
          | factor tryMultDivQuadruple '/' pushOperation term'''

# pending UMINUS
def p_factor(p):
  '''factor : '(' addFakeBottom super_expression removeFakeBottom ')'
            | value'''

def p_value(p):
  '''value : constant addConstant pushConstantOperand
           | ID lookupId pushIdOperand
           | function_call'''

# ===== Constants =====
def p_constant_int(p):
    "constant : CTE_INT"
    p[0] = int(p[1])

def p_constant_boolean(p):
    '''constant : FALSE
                | TRUE'''
    if p[1] == 'false':
        p[0] = False
    elif p[1] == 'true':
        p[0] = True

def p_constant_float(p):
    "constant : CTE_FLOAT"
    p[0] = float(p[1])

def p_constant_strings(p):
    '''constant : CTE_STRING
                | CTE_CHAR'''
    p[0] = str(p[1])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
    summary()
    exit(1)

# =============== Grammar Actions START ===============

def p_setLocalScope(p):
  'setLocalScope :'
  setLocalScope()

def p_setGlobalScope(p):
  'setGlobalScope :'
  setGlobalScope()

def p_saveVariableType(p):
  'saveVariableType :'
  global __tVarType
  __tVarType = p[-1]

def p_addVariable(p):
  'addVariable :'
  global __tVarName
  __tVarName = p[-1]
  addVariable(__tVarName, __tVarType)

def p_addConstant(p):
  'addConstant :'
  constRaw = p[-1]
  addConstant(constRaw)

def p_setTypeAsArray(p):
  'setTypeAsArray :'
  setTypeAsArray()

def p_lookupId(p):
  'lookupId :'
  global __tVarName, __tVarType

  operandID = p[-1]
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(operandID)
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(operandID)

  if variable is None:
    print("Variable error: variable not found")
    summary()
    exit(1)
    return
  else:
    __tVarName = variable.name
    __tVarType = variable.symbolType

# === Expressions ==

def p_pushOperation(p):
  'pushOperation :'
  __operationStack.push(p[-1])

def p_pushIdOperand(p):
  'pushIdOperand :'
  __operandStack.push(__tVarName)
  __typeStack.push(__tVarType)

def p_pushConstantOperand(p):
  'pushConstantOperand :'
  constName = str(p[-2])
  constant = __constantTable.lookup(constName)
  if constant is not None:
    __operandStack.push(constant.name)
    __typeStack.push(constant.symbolType)
  else:
    print "Constant error: constant not found", constName

def p_tryLogicalQuadruple(p):
  'tryLogicalQuadruple :'
  addExpressionQuadruple(['and', 'or'])

def p_tryRelationalQuadruple(p):
  'tryRelationalQuadruple :'
  addExpressionQuadruple(['<', '>', '==', '!=', '<=', '>='])

def p_tryAddSubQuadruple(p):
  'tryAddSubQuadruple :'
  addExpressionQuadruple(['+', '-'])

def p_tryMultDivQuadruple(p):
  'tryMultDivQuadruple :'
  addExpressionQuadruple(['*', '/', '%'])

def p_addFakeBottom(p):
  'addFakeBottom :'
  __operationStack.push('(')

def p_removeFakeBottom(p):
  'removeFakeBottom :'
  __operationStack.pop()

def p_addAssignmentQuadruple(p):
  'addAssignmentQuadruple :'
  operator = __operationStack.pop()
  # Operands
  rightOp = __operandStack.pop()
  leftOp = __operandStack.pop()
  # Types
  rightType = __typeStack.pop()
  leftType = __typeStack.pop()
  resultType = getResultType(leftType, operator, rightType)
  if resultType is not None:
    # Generate quadruple
    __quadruples.add(Quadruple(operator, rightOp, None, leftOp))
  else:
    print "Expression error : result type mismatch"
    summary()
    exit(1)

# == Conditionals == 

def p_ifConditional(p):
  'ifConditional :'
  conditionalType = __typeStack.pop()
  if conditionalType == Type.BOOL:
    result = __operandStack.pop()
    __quadruples.add(Quadruple('GOTOF', result, None, -1))
    # Save if position
    __jumpStack.push(__quadruples.size()-1)
  else:
    print "Conditional error : result type mismatch"
    summary()
    exit(1)

def p_endIfConditional(p):
  'endIfConditional :'
  setLastJumpPosition(__quadruples.size())

def p_elseConditional(p):
  'elseConditional :'
  __quadruples.add(Quadruple('GOTO', None, None, -1))
  # Set else position
  setLastJumpPosition(__quadruples.size())
  # Save goto position
  __jumpStack.push(__quadruples.size()-1)

def p_elseIfConditional(p):
  'elseIfConditional :'
  setLastJumpPosition(__quadruples.size() + 1)
  setLastJumpPosition(__quadruples.size())
  __quadruples.add(Quadruple('GOTO', None, None, -1))
  # Save goto position
  __jumpStack.push(__quadruples.size()-1)

def p_endElseIfConditional(p):
  'endElseIfConditional :'
  setLastJumpPosition(__quadruples.size())
  setLastJumpPosition(__quadruples.size())

# == Loops == 

def p_startLoop(p):
  'startLoop :'
  __jumpStack.push(__quadruples.size())

def p_loopConditional(p):
  'loopConditional : ifConditional'

def p_endLoop(p):
  'endLoop :'
  lastWhilePos = __jumpStack.pop()
  returnPos = __jumpStack.pop()
  __quadruples.add(Quadruple('GOTO', None, None, returnPos))
  lastWhileQ = __quadruples.list[lastWhilePos]
  lastWhileQ.result = __quadruples.size()
  print "__ Update ", lastWhilePos, " result to ", __quadruples.size()

# == Functions

def p_saveFunctionType(p):
  'saveFunctionType :'
  global __tFuncType
  __tFuncType = p[-1]

def p_saveFunctionName(p):
  'saveFunctionName :'
  global __tFuncName
  __tFuncName = p[-1]

def p_endFunction(p):
  'endFunction :'
  global __tFuncParameters
  __varsLocal.clear()
  __tFuncParameters = []
  __quadruples.add(Quadruple('ENDPROC', None, None, None))

def p_addParameter(p):
  'addParameter :'
  global __tVarName
  global __tFuncParameters
  __tVarName = p[-1]
  addVariable(__tVarName, __tVarType)
  __tFuncParameters.append(__varsLocal.lookup(__tVarName))

def p_addFunction(p):
  'addFunction :'
  addFunction(__tFuncName, __tFuncType, __tFuncParameters, __quadruples.size())
  # print('Local Variables: %s' % __varsLocal)

def p_lookupFunctionId(p):
  'lookupFunction :'
  global __tCallName, __tCallType
  functionId = p[-2]
  function = __funcsGlobal.lookup(functionId)
  if function is not None:
    __tCallName = function.name
    __tCallType = function.functionType
  else:
    print("Function error: function not found")
    summary()
    exit(1)

def p_startFunctionCall(p):
  'startFunctionCall :'
  global __tCallArgCount
  __quadruples.add(Quadruple("ERA", __tFuncName, None, None))
  __tCallArgCount = 0

def p_addArgument(p):
  'addArgument :'
  global __tCallArgCount
  argument = __operandStack.pop()
  argumentType = __typeStack.pop()
  function = __funcsGlobal.lookup(__tCallName)
  parameter = function.parameters[__tCallArgCount]
  if argumentType == parameter.symbolType:
    __quadruples.add(Quadruple('PARAM', argument, None, __tCallArgCount))
    __tCallArgCount += 1 
  else:
    print "Function error: parameter type mismatch"
    summary()
    exit(1)

# def p_increaseArguments(p):
#   'increaseArguments :'
#   global __tCallArgCount
    # __tCallArgCount += 1 

def p_verifyArguments(p):
  'verifyArguments :'
  function = __funcsGlobal.lookup(__tCallName)
  if function.parametersSize() != __tCallArgCount:
    print "Function error: incorrect number of arguments"
    summary()
    exit(1)

def p_endFunctionCall(p):
  'endFunctionCall :'
  function = __funcsGlobal.lookup(__tCallName)
  if function is not None:
    __quadruples.add(Quadruple('GOSUB', __tCallName, None, function.quadruplePosition))
  else:
    print "Function error: function not found"

def p_checkForReturn(p):
  'checkForReturn :'
  if __tCallType != Type.VOID and __tCallType != None:
    address =  __memory.generateTemporary(__tCallType)
    __quadruples.add(Quadruple('=', __tCallName, None, address))
    __operandStack.push(address)
    __typeStack.push(__tCallType)

def p_returnFunctionValue(p):
  'returnFunctionValue :'
  returnType = __typeStack.pop()
  returnValue = __operandStack.pop()
  if returnType == __tFuncType:
    __quadruples.add(Quadruple('RETURN', None, None, returnValue))
  else:
    print "Function error: return type mismatch"
    summary()
    exit(1)

# =============== Grammar Actions END ===============

# Pops the jump stack ands sets that quadruples result to a position
def setLastJumpPosition(position):
  lastPos = __jumpStack.pop()
  quadruple = __quadruples.list[lastPos]
  quadruple.result = position
  print "__ Update ", lastPos, " result to ", position

# Create the quadruple for the requests operators
def addExpressionQuadruple(operators):
  global __operationStack, __operandStack, __typeStack
  operator = __operationStack.top()
  if operator in operators:
    operator = __operationStack.pop()
    # Operands
    rightOp = __operandStack.pop()
    leftOp = __operandStack.pop()
    # Types
    rightType = __typeStack.pop()
    leftType = __typeStack.pop()
    resultType = getResultType(leftType, operator, rightType)
    if resultType is not None:
      # Generate quadruple
      address =  __memory.generateTemporary(resultType)
      __quadruples.add(Quadruple(operator, leftOp, rightOp, address))
      # Update stacks
      __operandStack.push(address)
      __typeStack.push(resultType)
    else:
      summary()
      exit(1)

def addVariable(name, varType):
  global __varsGlobal, __varsLocal
  if varType == Type.VOID:
    print "Variable error : can't be of VOID type"
    return
  
  variable = Var(name, varType)
  if __scope == Scope.GLOBAL:
    # Construct variable globally
    __varsGlobal.insert(variable)
    variable.id = __memory.generateGlobal(varType)
  elif __scope == Scope.LOCAL:
    # Construct variable locally
    __varsLocal.insert(variable)
    variable.id = __memory.generateLocal(varType)

def addConstant(const):
  global __constantTable
  # Scan raw
  if __constantTable.lookup(str(const)) is None:
    if isinstance(const, bool):  
      constType = Type.BOOL
      constValue = const
    elif isinstance(const, int):  
      constType = Type.INT
      constValue = const
    elif isinstance(const, float):  
      constType = Type.FLOAT
      constValue = const
    elif isinstance(const, str) and len(str(const)) == 3:  
      constType = Type.CHAR
      constValue = str(const)
    else:  
      constType = Type.STRING
      constValue = str(const)
    # Create constant
    c = __constantTable.insert(Constant(str(const), constType, constValue))
    c.id = __memory.generateConstant(constType)

def addFunction(functionName, functionType, parameters, position):
  global __funcsGlobal
  function = Function(functionName, functionType, parameters, position)
  __funcsGlobal.insert(function)

def setTypeAsArray():
  if __scope == Scope.GLOBAL:
    global __varsGlobal
    variable = __varsGlobal.lookup(__tVarName)
    variable.setIsArray(True)
  elif __scope == Scope.LOCAL:
    global __varsLocal
    variable = __varsLocal.lookup(__tVarName)
    variable.setIsArray(True)

# =============== Execution ===============

yacc.yacc()

def summary():
  print "================================ START SUMMARY ================================:"
  print "_________Quadruples_________:"
  print __quadruples
  print "_________  Stacks  _________:"
  print "Operations:", __operationStack
  print "Operands:", __operandStack
  print "Types:", __typeStack
  print "Jump:", __jumpStack
  print "_________  Tables  _________:"
  print "G-VARS: (", __varsGlobal.size(), ")", __varsGlobal
  print "L-VARS: (", __varsLocal.size(), ")", __varsLocal
  print "CONSTS: (", __constantTable.size(), ")", __constantTable
  print "G-FUNCS:", __funcsGlobal
  print "================================ END SUMMARY ================================\n"

# Main Method
if __name__ == '__main__':
  if (len(sys.argv) > 1):
    file = sys.argv[1]
    # Open file
    try:
      f = open(file, 'r')
      data = f.read()
      f.close()
      # Parse the data
      if (yacc.parse(data, tracking = True) == 'OK'):
        print(dirProc);
      summary()
    except EOFError:
      print(EOFError)
  else:
    while 1:
      try:
        s = raw_input('craft > ')
        s = "craft { " + s + "}"
      except EOFError:
        break
      if not s:
        continue
      yacc.parse(s)
      summary()

