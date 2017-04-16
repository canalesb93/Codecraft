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

# Variable Memory Counter Maps

__tempVarCount = {}
__tempVarCount[Type.BOOL] = 0
__tempVarCount[Type.INT] = 0
__tempVarCount[Type.FLOAT] = 0
__tempVarCount[Type.CHAR] = 0
__tempVarCount[Type.STRING] = 0

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
__tFuncArguments = []
__tVarType = None
__tFuncType = None
__tVarName = None
__tFuncName = None
__tVarIsArray = False

# Scope
__scope = Scope.GLOBAL

def setLocalScope():
  global __scope 
  __scope = Scope.LOCAL

def setGlobalScope():
  global __scope 
  __scope = Scope.GLOBAL

# =============== Global END ===============

# =============== Grammar START ===============

def p_program(p):
    'program : CRAFT "{" block functions "}"'

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

def p_functions(p):
    '''functions : function functions
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
    ''' function : FUNCTION setLocalScope type saveFunctionType ID saveFunctionName "(" parameters_definition ")" "{" block "}" setGlobalScope
                 ''' 
    global __tFuncArguments
    addFunction(__tFuncName, __tFuncType, __tFuncArguments)
    # print('Local Variables: %s' % __varsLocal)
    __varsLocal.clear()
    __tFuncArguments = []

def p_parameters_definition(p):
    '''parameters_definition : type saveVariableType ID addArgument parameters_definition1
                             | empty''' 
    pass

def p_parameters_definition1(p):
    '''parameters_definition1 : "," type saveVariableType ID addArgument parameters_definition1
                              | empty'''
    pass

def p_parameters(p):
    '''parameters : super_expression parameters1
                  | empty'''
    pass

def p_parameters1(p):
    '''parameters1 : "," super_expression parameters1
                   | empty'''
    pass

def p_block(p):
    '''block : vars block
             | var_free_assignment block
             | if block
             | cycle block
             | return block
             | BREAK block
             | CONTINUE block
             | function_call block
             | empty'''
    pass

def p_if(p):
    '''if : IF "(" super_expression ")" "{" block "}"
          | IF "(" super_expression ")" "{" block "}" else'''
    pass

def p_else(p):
    '''else : ELSE if
            | ELSE "{" block "}"'''
    pass

def p_cycle(p):
    'cycle : WHILE "(" super_expression ")" "{" block "}"'
    pass

def p_return(p):
    '''return : RETURN
              | RETURN super_expression'''
    pass

def p_function_call(p):
    '''function_call : ID "(" ")" 
                     | ID "(" parameters ")"'''
    pass

# ===== Binary Operations (cascades through here) =====

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

# Constants
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

# =============== Grammar Actions START ===============

def p_setLocalScope(p):
  'setLocalScope :'
  setLocalScope()

def p_setGlobalScope(p):
  'setGlobalScope :'
  setGlobalScope()

def p_saveFunctionType(p):
  'saveFunctionType :'
  global __tFuncType
  __tFuncType = p[-1]

def p_saveFunctionName(p):
  'saveFunctionName :'
  global __tFuncName
  __tFuncName = p[-1]

def p_addArgument(p):
  'addArgument :'
  global __tVarName
  global __tFuncArguments
  __tVarName = p[-1]
  addVariable(__tVarName, __tVarType)
  __tFuncArguments.append(__varsLocal.lookup(__tVarName))

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

# == Quadruples ==

def p_pushOperation(p):
  'pushOperation :'
  global __operationStack
  __operationStack.push(p[-1])

def p_pushIdOperand(p):
  'pushIdOperand :'
  global __operandStack, __typeStack
  __operandStack.push(__tVarName)
  __typeStack.push(__tVarType)

def p_pushConstantOperand(p):
  'pushConstantOperand :'
  global __operandStack, __typeStack
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
  global __operationStack
  __operationStack.push('(')

def p_removeFakeBottom(p):
  'removeFakeBottom :'
  global __operationStack
  __operationStack.pop()

def p_addAssignmentQuadruple(p):
  'addAssignmentQuadruple :'
  global __operationStack, __operandStack, __typeStack
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

# =============== Grammar Actions END ===============

# Create the quadruple for the requests operators
def addExpressionQuadruple(operators):
  global __operationStack, __operandStack, __typeStack
  global __tempVarCount
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
      __quadruples.add(Quadruple(operator, leftOp, rightOp, resultType.name.lower() + str(__tempVarCount[resultType])))
      # Update stacks
      __operandStack.push(resultType.name.lower() + str(__tempVarCount[resultType]))
      __typeStack.push(resultType)
      __tempVarCount[resultType] += 1
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
  elif __scope == Scope.LOCAL:
    # Construct variable locally
    __varsLocal.insert(variable)

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
    __constantTable.insert(Constant(str(const), constType, constValue))

def addFunction(functionName, functionType, parameters):
  global __funcsGlobal
  function = Function(functionName, functionType, parameters)
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
  print "_________QUADRUPLES_________:"
  print __quadruples
  print "_________Stacks_________:"
  print "Operations:", __operationStack
  print "Operands:", __operandStack
  print "Types:", __typeStack
  print "Jump:", __jumpStack
  print "_________Tables_________:"
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

