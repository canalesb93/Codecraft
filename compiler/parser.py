#!python2
# -----------------------------------------------------------------------------
# parser.py
#
# Author: Ricardo Canales and Gabriel Berlanga
#
# The main module for the CodeCraft programming language compilation phase.
# Parses and generates the OBJ file for the inputed file
# -----------------------------------------------------------------------------

import sys
import csv
import scanner
from libraries.ply import lex
from libraries.ply import yacc

# Classes
from enumerators import *
from classes import *
from cube import *
from memory import AddressSystem

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Setup
#
# Prepend "__" to all global variables for easy undestanding. Remember to 
# use "global" when modifying these variables in a different scope.
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////

if sys.version_info[0] >= 3:
    raw_input = input

tokens = scanner.tokens
lex.lex(module=scanner)

# =============================================================================
# Global
# =============================================================================

# Quadruple Setup
__quadruples = QuadrupleList()
__operandStack = Stack()
__operationStack = Stack()
__typeStack = Stack()
__jumpStack = Stack()

# Temporary Var/Func data
# Vars
__tVarType = Stack()
__tVarName = Stack()
__tVarArrDim = Stack()
# Funcs
__tFuncName = None
__tFuncType = None
__tFuncParameters = []
# Func Calls
__tCallName = Stack()
__tCallType = Stack()
__tCallArgCount = Stack()

# Symbol Tables
__constantTable = SymbolTable()
__varsGlobal = SymbolTable()
__varsLocal = SymbolTable()
__funcsGlobal = FunctionTable()
__address = AddressSystem()

# Scope
__scope = Scope.GLOBAL


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Grammar Rules
#
# Defines the semantic behavior the programing language should follow. 
# Format: Rules use TOKENS for matching, other_rules for recursion and
# grammarActions for actions. Modifying rules can be hard and must consider
# Grammar Actions usge when doing so.
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////

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

# =============================================================================
# Variables
# =============================================================================

def p_vars(p):
  '''vars : VAR type saveVariableType var eraseVariableType'''

def p_var(p):
  '''var : ID saveVariableName addVariable var_array_init var_assignment eraseVariableName var_repeater
         '''

def p_var_repeater(p):
  '''var_repeater : "," var
                  | empty
                  '''

def p_var_assignment(p):
  '''var_assignment : pushIdOperand "=" pushOperation super_expression addAssignmentQuadruple
                    | empty'''

def p_var_free_assignment(p):
  '''var_free_assignment : ID lookupId pushIdOperand eraseVariableName eraseVariableType "=" pushOperation super_expression addAssignmentQuadruple'''

# =============================================================================
# Arrays
# =============================================================================

def p_var_array_init(p):
  '''var_array_init : var_array_dimension generateDimensionSpace
                    | empty'''

def p_var_array_dimension(p):
  '''var_array_dimension : "[" CTE_INT addDimension "]" var_array_dimension1'''

def p_var_array_dimension1(p):
  '''var_array_dimension1 : "[" CTE_INT addDimension "]" var_array_dimension1
                          | empty'''

# def p_assignment_array(p):
#     '''assignment_array : ID "=" "{" parameters "}" ',' assignment
#                         | ID "=" "{" parameters "}" 
#                         | ID
#                         '''

def p_var_arr_free_assignment(p):
  '''var_arr_free_assignment : ID lookupId index_selector "=" pushOperation super_expression addAssignmentQuadruple'''

def p_index_selector(p):
  '''index_selector : saveVariableDimension "[" addFakeBottom exp removeFakeBottom validateArrayIndex "]" index_selector1 addAddressBase eraseVariableName eraseVariableType eraseVariableDimension'''

def p_index_selector1(p):
  '''index_selector1 : offsetForDimension "[" addFakeBottom exp removeFakeBottom validateArrayIndex "]" accummulateDisplacement index_selector1
                     | empty'''

# =============================================================================
# Functions
# =============================================================================

def p_function(p):
  ''' function : FUNCTION setLocalScope type saveFunctionType ID saveFunctionName "(" parameters_definition ")" addFunction "{" block_repeater "}" endFunction setGlobalScope
               ''' 

def p_parameters_definition(p):
  '''parameters_definition : type ID addParameter parameters_definition1
                           | empty''' 

def p_parameters_definition1(p):
  '''parameters_definition1 : "," type ID addParameter parameters_definition1
                            | empty'''

def p_parameters(p):
  '''parameters : super_expression addArgument parameters1
                | empty'''

def p_parameters1(p):
  '''parameters1 : "," super_expression addArgument parameters1
                 | empty'''

def p_return(p):
  '''return : RETURN returnFunction
            | RETURN super_expression returnFunctionValue'''

def p_function_call(p):
  '''function_call : ID "(" lookupFunction startFunctionCall addFakeBottom parameters removeFakeBottom ")" verifyArguments endFunctionCall
                   | ID "(" lookupFunction startFunctionCall ")" endFunctionCall'''

def p_block_repeater(p):
  '''block_repeater : block block_repeater
                    | empty'''

def p_block(p):
  '''block : vars
           | var_free_assignment
           | var_arr_free_assignment
           | if
           | cycle
           | return
           | BREAK
           | CONTINUE
           | output
           | input
           | function_call'''

def p_output(p):
  '''output : OUTPUT "(" super_expression addOutputQuadruple output1 ")"
            | OUTPUTLN "(" super_expression addOutputQuadruple output1 addNewLineQuadruple ")"
            | OUTPUTLN addNewLineQuadruple'''

def p_output1(p):
  '''output1 : "," super_expression addOutputQuadruple output1
             | empty'''

def p_input(p):
  ''' input : INPUT "(" ID lookupId pushIdOperand eraseVariableName eraseVariableType ")" addInputQuadruple
            | INPUT "(" ID lookupId index_selector ")" addInputQuadruple'''

# =============================================================================
# Conditionals and Loops
# =============================================================================

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

# =============================================================================
# Expressions
# 
# Defines expression rules. Follows a recursive precedence starting at
# 'super_expression' (first rule is last quadruple generated):
# 
# Logical -> Relational -> Sum/Sub -> Mult/Div -> uMinus -> Parenthesis
# -> value,id,function_calls
# 
# =============================================================================

def p_super_expression(p):
  '''super_expression : expression tryLogicalQuadruple
                      | expression tryLogicalQuadruple AND pushOperation super_expression
                      | expression tryLogicalQuadruple OR pushOperation super_expression'''

def p_expression(p):
  '''expression : exp tryRelationalQuadruple
                | exp tryRelationalQuadruple '>' pushOperation expression
                | exp tryRelationalQuadruple '<' pushOperation expression
                | exp tryRelationalQuadruple EQ pushOperation expression
                | exp tryRelationalQuadruple UNEQ pushOperation expression
                | exp tryRelationalQuadruple LESS_EQ pushOperation expression
                | exp tryRelationalQuadruple GREATER_EQ pushOperation expression'''

def p_exp(p):
  '''exp : term tryAddSubQuadruple
         | term tryAddSubQuadruple '+' pushOperation exp
         | term tryAddSubQuadruple '-' pushOperation exp '''

def p_term(p):
  '''term : uminus tryMultDivQuadruple
          | uminus tryMultDivQuadruple '*' pushOperation term
          | uminus tryMultDivQuadruple '/' pushOperation term
          | uminus tryMultDivQuadruple '%' pushOperation term'''

def p_uminus(p):
  '''uminus : '-' factor generateUMinusQuadruple 
            | factor'''

def p_factor(p):
  '''factor : '(' addFakeBottom super_expression removeFakeBottom ')'
            | value'''

def p_value(p):
  '''value : constant addConstant pushConstantOperand
           | ID lookupId pushIdOperand eraseVariableName eraseVariableType
           | ID lookupId index_selector
           | function_call'''       

# =============================================================================
# Constants
# =============================================================================

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
              | CTE_CHAR '''
  p[0] = str(p[1])[1:-1].decode('string_escape')

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

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Grammar Actions
#
# These actions are empty grammar rules. They are called by other grammar 
# rules and access values retreived by them. They perform actions ranging
# from quadruple generation to tables management(var)
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////

# Sets the scope to local
def p_setLocalScope(p):
  'setLocalScope :'
  global __scope 
  __scope = Scope.LOCAL

# Sets the scope to global
def p_setGlobalScope(p):
  'setGlobalScope :'
  global __scope 
  __scope = Scope.GLOBAL

# =============================================================================
# Variable/Constant Actions
# =============================================================================

# Stores the variable type in the temporary stacks
def p_saveVariableType(p):
  'saveVariableType :'
  __tVarType.push(p[-1])

# Pops a variable type from the temporary stacks
def p_eraseVariableType(p):
  'eraseVariableType :'
  __tVarType.pop()

# Stores the variable id in the temporary stacks
def p_saveVariableName(p):
  'saveVariableName :'
  __tVarName.push(p[-1])

# Pops a variable id from the temporary stacks
def p_eraseVariableName(p):
  'eraseVariableName :'
  __tVarName.pop()

# Stores the index dimension in the temporary stacks
def p_saveVariableDimension(p):
  'saveVariableDimension :'
  __tVarArrDim.push(0)

# Pops the index dimension from the temporary stacks
def p_eraseVariableDimension(p):
  'eraseVariableDimension :'
  __tVarArrDim.pop()

# Sends variable data to variable creation method
def p_addVariable(p):
  'addVariable :'
  addVariable(__tVarName.top(), __tVarType.top())

# Sends constant data to constant creation method
def p_addConstant(p):
  'addConstant :'
  constRaw = p[-1]
  addConstant(constRaw)

# Searches the variable symbol table for the ID
def p_lookupId(p):
  'lookupId :'
  operandID = p[-1]
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(operandID)
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(operandID)
    if variable is None:
      variable = __varsGlobal.lookup(operandID)

  if variable is None:
    print "Variable error: variable not found", operandID
    summary()
    exit(1)
    return
  else:
    __tVarName.push(variable.name)
    __tVarType.push(variable.symbolType)

# Creates a simple newline quadruple
def p_addNewLineQuadruple(p):
  'addNewLineQuadruple :'
  __quadruples.add(Quadruple("OUTPUTLN", None, None, None))

# =============================================================================
# Array Actions
# =============================================================================

# Adds a dimension to a lookedup variable, making it an array
def p_addDimension(p):
  'addDimension :'
  size = int(p[-1])
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(__tVarName.top())
    variable.addDimension(size)
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(__tVarName.top())
    if variable is None:
      variable = __varsGlobal.lookup(__tVarName.top())
    variable.addDimension(size)

# Generates dimension addresses based on total dimension space in variable
def p_generateDimensionSpace(p):
  'generateDimensionSpace :'
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(__tVarName.top())
    # -1 for already defined address
    size = variable.totalSpace() - 1
    if size > 0:
      __address.generateGlobal(variable.symbolType, size)
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(__tVarName.top())
    if variable is None:
      variable = __varsGlobal.lookup(__tVarName.top())
    size = variable.totalSpace() - 1
    if size > 0:
      __address.generateLocal(variable.symbolType, size)

# Generates index validation quadruple 
def p_validateArrayIndex(p):
  'validateArrayIndex :'
  dimension = __tVarArrDim.pop()
  index = __operandStack.top()
  if __typeStack.top() is not Type.INT:
    print "Array error: index should be integer"
    summary()
    exit(1)
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(__tVarName.top())
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(__tVarName.top())
    if variable is None:
      variable = __varsGlobal.lookup(__tVarName.top())
  if (dimension >= variable.dimensionCount()):
    print "Array error: incorrect dimension count"
    summary()
    exit(1)
  __quadruples.add(Quadruple("VER", index, 0, variable.dimensions[dimension]))
  __tVarArrDim.push(dimension + 1)

# Generates offset quadruple for multiple dimensioned arrays
def p_offsetForDimension(p):
  'offsetForDimension :'
  dimension = __tVarArrDim.pop() - 1
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(__tVarName.top())
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(__tVarName.top())
    if variable is None:
      variable = __varsGlobal.lookup(__tVarName.top())
    # Operands
  leftOp = __operandStack.pop()
  leftType = __typeStack.pop()
  limit = variable.dimensions[dimension]
  addConstant(limit)
  c = __constantTable.lookup(str(limit))
  # Generate quadruple
  if __scope == Scope.GLOBAL:
    address =  __address.generateGlobalTemporary(Type.INT)
  elif __scope == Scope.LOCAL:
    address =  __address.generateTemporary(Type.INT)
  __quadruples.add(Quadruple('*', leftOp, c.address(), address))
  # Update stacks
  __operandStack.push(address)
  __typeStack.push(Type.INT)
  __tVarArrDim.push(dimension + 1)

# Generates displacement quadruple for array index address
def p_accummulateDisplacement(p):
  'accummulateDisplacement :'
  rightOp = __operandStack.pop()
  leftOp = __operandStack.pop()
  # Unused Types
  __typeStack.pop()
  __typeStack.pop()
  if __scope == Scope.GLOBAL:
    address =  __address.generateGlobalTemporary(Type.INT)
  elif __scope == Scope.LOCAL:
    address =  __address.generateTemporary(Type.INT)
  __quadruples.add(Quadruple('+', leftOp, rightOp, address))
  __operandStack.push(address)
  __typeStack.push(Type.INT)

# Adds variable base address quadruple for array index address# 
def p_addAddressBase(p):
  'addAddressBase :'
  leftOp = __operandStack.pop()
  __typeStack.pop()
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(__tVarName.top())
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(__tVarName.top())
    if variable is None:
      variable = __varsGlobal.lookup(__tVarName.top())
  if __scope == Scope.GLOBAL:
    address =  __address.generateGlobalTemporary(Type.INT)
  elif __scope == Scope.LOCAL:
    address =  __address.generateTemporary(Type.INT)
  address = '(' + str(address) + ')'
  __quadruples.add(Quadruple('ACUM', leftOp, variable.address(), address))
  __operandStack.push(address)
  __typeStack.push(variable.symbolType)

# =============================================================================
# Expression Actions
# =============================================================================

# Pushes operation to operationStack
def p_pushOperation(p):
  'pushOperation :'
  __operationStack.push(p[-1])

# Pushes variable address to operandStack
def p_pushIdOperand(p):
  'pushIdOperand :'
  if __scope == Scope.GLOBAL:
    variable = __varsGlobal.lookup(__tVarName.top())
    if variable is None:
      print "GlobalVar error: variable not found"
  elif __scope == Scope.LOCAL:
    variable = __varsLocal.lookup(__tVarName.top())
    if variable is None:
      variable = __varsGlobal.lookup(__tVarName.top())
    if variable is None:
      print "LocalVar error: variable not found"
  __operandStack.push(variable.address())
  __typeStack.push(__tVarType.top())

# Pushes constant address to operandStack
def p_pushConstantOperand(p):
  'pushConstantOperand :'
  constName = str(p[-2])
  constant = __constantTable.lookup(constName)
  if constant is not None:
    __operandStack.push(constant.address())
    __typeStack.push(constant.symbolType)
  else:
    print "Constant error: constant not found", constName

# Tries to generate a logical expression
def p_tryLogicalQuadruple(p):
  'tryLogicalQuadruple :'
  addExpressionQuadruple(['and', 'or'])

# Tries to generate a relational expression
def p_tryRelationalQuadruple(p):
  'tryRelationalQuadruple :'
  addExpressionQuadruple(['<', '>', '==', '!=', '<=', '>='])

# Tries to generate a add/sub expression
def p_tryAddSubQuadruple(p):
  'tryAddSubQuadruple :'
  addExpressionQuadruple(['+', '-'])

# Tries to generate a mult/div expression
def p_tryMultDivQuadruple(p):
  'tryMultDivQuadruple :'
  addExpressionQuadruple(['*', '/', '%'])

# Generates 'uminus' quadruple
def p_generateUMinusQuadruple(p):
  'generateUMinusQuadruple :'
  rightOp = __operandStack.pop()
  t = __typeStack.pop()
  if t is Type.BOOL or t is Type.CHAR or t is Type.STRING:
    print "Arithmetic error: can't negate expression"
    summary()
    exit(1)
  addConstant(-1)
  c = __constantTable.lookup("-1")
  resultType = getResultType(c.symbolType, "*", t)
  if __scope == Scope.GLOBAL:
    address =  __address.generateGlobalTemporary(Type.INT)
  elif __scope == Scope.LOCAL:
    address =  __address.generateTemporary(Type.INT)
  __quadruples.add(Quadruple('*', c.address(), rightOp, address))
  __operandStack.push(address)
  __typeStack.push(resultType)

# Adds the 'fake' bottom to operationStack
def p_addFakeBottom(p):
  'addFakeBottom :'
  __operationStack.push('(')

# Removes the 'fake' bottom from operaitonStack
def p_removeFakeBottom(p):
  'removeFakeBottom :'
  __operationStack.pop()

# Generates assignment quadruple
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

# =============================================================================
# Conditional Actions
# =============================================================================

# Generates GOTOF quadruple, adds location to jumpStack
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

# Updates last jump position to current position
def p_endIfConditional(p):
  'endIfConditional :'
  setLastJumpPosition(__quadruples.size())

# Generates a GOTO quadruple, updates last jump position and adds current
# position to jump stack
def p_elseConditional(p):
  'elseConditional :'
  __quadruples.add(Quadruple("GOTO", None, None, -1))
  # Set else position
  setLastJumpPosition(__quadruples.size())
  # Save goto position
  __jumpStack.push(__quadruples.size()-1)

# Updates last 2 jump positions and generates GOTO quadruple, adds current 
# position to jumpStack
def p_elseIfConditional(p):
  'elseIfConditional :'
  setLastJumpPosition(__quadruples.size() + 1)
  setLastJumpPosition(__quadruples.size())
  __quadruples.add(Quadruple("GOTO", None, None, -1))
  # Save goto position
  __jumpStack.push(__quadruples.size()-1)

# Updates last 2 jump positions to current position
def p_endElseIfConditional(p):
  'endElseIfConditional :'
  setLastJumpPosition(__quadruples.size())
  setLastJumpPosition(__quadruples.size())

# Pushes current position to jumpStack
def p_startLoop(p):
  'startLoop :'
  __jumpStack.push(__quadruples.size())

# Generates GOTOF quadruple, adds location to jumpStack (same as ifConditional)
def p_loopConditional(p):
  'loopConditional : ifConditional'

# Sets jump to start of loop and then updates conditional to end of loop
def p_endLoop(p):
  'endLoop :'
  lastWhilePos = __jumpStack.pop() # loop conditional position
  returnPos = __jumpStack.pop() # start of loop position
  __quadruples.add(Quadruple('GOTO', None, None, returnPos))
  lastWhileQ = __quadruples.list[lastWhilePos]
  lastWhileQ.result = __quadruples.size()
  print "__ Update ", lastWhilePos, " result to ", __quadruples.size()

# =============================================================================
# Function Actions
# =============================================================================

# Save function type to temporary variable
def p_saveFunctionType(p):
  'saveFunctionType :'
  global __tFuncType
  __tFuncType = p[-1]

# Save function id to temporary variable
def p_saveFunctionName(p):
  'saveFunctionName :'
  global __tFuncName
  __tFuncName = p[-1]

# Clears all local data, sets the functions address limit, generates ENDPROC
def p_endFunction(p):
  'endFunction :'
  global __tFuncParameters
  __varsLocal.clear()
  f = __funcsGlobal.lookup(__tFuncName)
  f.limits = __address.retrieveLocalLimits()
  __tFuncParameters = []
  __quadruples.add(Quadruple('ENDPROC', None, None, None))
  setLastJumpPosition(__quadruples.size())

# Creates variable in local scope, appends parameter to temporary list
def p_addParameter(p):
  'addParameter :'
  varName = p[-1]
  varType = p[-2]
  addVariable(varName, varType)
  __tFuncParameters.append(__varsLocal.lookup(varName))

# Adds SKIP quadruple with pos to jumpStack, creates function object
def p_addFunction(p):
  'addFunction :'
  __quadruples.add(Quadruple("SKIP", None, None, -1))
  __jumpStack.push(__quadruples.size()-1)
  addFunction(__tFuncName, __tFuncType, __tFuncParameters, __quadruples.size())

# Lookup function in functionTable, adds name and type to temporary stacks
def p_lookupFunctionId(p):
  'lookupFunction :'
  functionId = p[-2]
  function = __funcsGlobal.lookup(functionId)
  if function is not None:
    __tCallName.push(function.name)
    __tCallType.push(function.functionType)
  else:
    print("Function error: function not found")
    summary()
    exit(1)

# Generates ERA quadruple, sets argument count to 0 in temporarry stack
def p_startFunctionCall(p):
  'startFunctionCall :'
  __quadruples.add(Quadruple("ERA", __tCallName.top(), None, None))
  __tCallArgCount.push(0)

# Adds verifies parameter type and adds PARAM quadruple, increases arg count
def p_addArgument(p):
  'addArgument :'
  argument = __operandStack.pop()
  argumentType = __typeStack.pop()
  function = __funcsGlobal.lookup(__tCallName.top())
  parameter = function.parameters[__tCallArgCount.top()]
  if argumentType == parameter.symbolType:
    argCount = __tCallArgCount.pop()
    __quadruples.add(Quadruple("PARAM", argument, None, argCount))
    __tCallArgCount.push(argCount + 1) 
  else:
    print "Function error: parameter type mismatch"
    summary()
    exit(1)

# Verifies the correct number of argument
def p_verifyArguments(p):
  'verifyArguments :'
  function = __funcsGlobal.lookup(__tCallName.top())
  if function.parametersSize() != __tCallArgCount.top():
    print "Function error: incorrect number of arguments"
    summary()
    exit(1)

# Generate GOSUB quadruple with return a temporary address if needed
# Clear all function call temporary stacks
def p_endFunctionCall(p):
  'endFunctionCall :'
  function = __funcsGlobal.lookup(__tCallName.top())
  if function is not None:
    if __tCallType.top() != Type.VOID and function.functionType != None:
      if __scope == Scope.GLOBAL:
        address =  __address.generateGlobalTemporary(function.functionType)
      elif __scope == Scope.LOCAL:
        address =  __address.generateTemporary(function.functionType)
      __operandStack.push(address)
      __typeStack.push(function.functionType)
      __quadruples.add(Quadruple('GOSUB', function.name, None, address))
    else:
      __quadruples.add(Quadruple('GOSUB', function.name, None, None))
  else:
    print "Function error: function not found"
  __tCallName.pop()
  __tCallType.pop()
  __tCallArgCount.pop()

# Generates RETURN quadruple with return value
def p_returnFunctionValue(p):
  'returnFunctionValue :'
  returnType = __typeStack.pop()
  returnValue = __operandStack.pop()
  if assignmentCompatible(returnType, __tFuncType):
    __quadruples.add(Quadruple('RETURN', None, None, returnValue))
  else:
    print "Function error: return type mismatch"
    summary()
    exit(1)

# Generates RETURN quadruple w/o return value (void)
def p_returnFunction(p):
  'returnFunction :'
  __quadruples.add(Quadruple('RETURN', None, None, None))

# Generate OUTPUT quadruple
def p_addOutputQuadruple(p):
  'addOutputQuadruple :'
  output = __operandStack.pop()
  __typeStack.pop()
  __quadruples.add(Quadruple("OUTPUT", None, None, output))

# Generate INPUT quadruple (with address)
def p_addInputQuadruple(p):
  'addInputQuadruple :'
  inp = __operandStack.pop()
  __typeStack.pop()
  __quadruples.add(Quadruple("INPUT", None, None, inp))

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Grammar Action Helpers
#
# These are helper function that may be used by multiple grammar actions.
# Like grammar actions some generate quadruples and manage stacks and tables.
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////


# -----------------------------------------------------------------------------
# setLastJumpPosition()
#
# Pops the jump stack ands sets that quadruples result to a position
# -----------------------------------------------------------------------------

def setLastJumpPosition(position):
  lastPos = __jumpStack.pop()
  quadruple = __quadruples.list[lastPos]
  quadruple.result = position
  print "__ Update ", lastPos, " result to ", position

# -----------------------------------------------------------------------------
# addExpressionQuadruple()
#
# Create the expression quadruple for the requested operators and 
# generate the addresses based on the type.
# -----------------------------------------------------------------------------

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
      if __scope == Scope.GLOBAL:
        address =  __address.generateGlobalTemporary(resultType)
      elif __scope == Scope.LOCAL:
        address =  __address.generateTemporary(resultType)
      __quadruples.add(Quadruple(operator, leftOp, rightOp, address))
      # Update stacks
      __operandStack.push(address)
      __typeStack.push(resultType)
    else:
      summary()
      exit(1)

# -----------------------------------------------------------------------------
# addVariable()
#
# Create a new variable for the current scope. Generate and assign the address.
# Adds variable to correct symbol table
# -----------------------------------------------------------------------------

def addVariable(name, varType):
  global __varsGlobal, __varsLocal
  if varType == Type.VOID:
    print "Variable error : can't be of VOID type"
    return
  
  variable = Var(name, varType)
  if __scope == Scope.GLOBAL:
    # Construct variable globally
    __varsGlobal.insert(variable)
    variable.id = __address.generateGlobal(varType)
  elif __scope == Scope.LOCAL:
    # Construct variable locally
    __varsLocal.insert(variable)
    variable.id = __address.generateLocal(varType)

# -----------------------------------------------------------------------------
# addConstant()
#
# Create a new constant and generate the address. Constant type is retrieved
# from python variable which was casted during the constants grammar rules.
# Adds constant to correct symbol table.
# -----------------------------------------------------------------------------

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
    elif isinstance(const, str) and len(const) == 1:
      constType = Type.CHAR
      constValue = const
    else:
      constType = Type.STRING
      constValue = const
    # Create constant
    cid = __address.generateConstant(constType)
    # Save Constant to table
    __constantTable.insert(Constant(cid ,str(const), constType, constValue))

# -----------------------------------------------------------------------------
# addFunction()
#
# Create a function object and add it to the function table.
# -----------------------------------------------------------------------------

def addFunction(functionName, functionType, parameters, position):
  global __funcsGlobal
  function = Function(functionName, functionType, parameters, position)
  f = __funcsGlobal.insert(function)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Compilation
#
# Main function, reads input file, prints debug summary. Exports compiled OBJ
# file with quadruples function table and constants.
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////

# Run YACC
yacc.yacc()

# -----------------------------------------------------------------------------
# summary()
#
# Print a large summary of the current status of all relevant data structurs
# during the compilation phase.
# -----------------------------------------------------------------------------

def summary():
  print "============================= COMPILATION SUMMARY ==========================="
  print "_________Quadruples_________:"
  print __quadruples
  print "_________  Stacks  _________:"
  print "Operations:", __operationStack
  print "Operands:", __operandStack
  print "Types:", __typeStack
  print "Jump:", __jumpStack
  print "Name:", __tVarName
  print "Type:", __tVarType
  print "DIM:", __tVarArrDim
  print "_________  Tables  _________:"
  print "G-VARS: (", __varsGlobal.size(), ")", __varsGlobal
  print "L-VARS: (", __varsLocal.size(), ")", __varsLocal
  print "CONSTS: (", __constantTable.size(), ")", __constantTable
  print "G-FUNCS:", __funcsGlobal
  print "================================ END SUMMARY ================================"

# -----------------------------------------------------------------------------
# export()
#
# Export all necessary data to a CSV file, change file ending to '.crafted'
# -----------------------------------------------------------------------------

def export(filename):
  with open(filename, 'wb') as fp:
    writer = csv.writer(fp, delimiter=',')
    # Export Pointer Limits
    writer.writerow(limitDictToArray(__address.gtempPointer))
    writer.writerow(limitDictToArray(__address.localPointer))
    writer.writerow(limitDictToArray(__address.globalPointer))
    writer.writerow(limitDictToArray(__address.constantPointer))
    writer.writerow(['END', "MEM_LIMITS"])
    # Export Quadruples
    for q in __quadruples.list:
      writer.writerow([q.operator, q.operand1, q.operand2, q.result])
    writer.writerow(['END', "QUADRUPLES"])
    # Export Main Memory
    for k, c in __constantTable.symbols.iteritems():
      writer.writerow([c.id, c.value])
    writer.writerow(['END', "CONSTANTS"])
    # Export Function Table
    for f in __funcsGlobal.functions.itervalues():
      writer.writerow([f.name, f.functionType.value, len(f.parameters), f.quadruplePosition])
      writer.writerow(limitDictToArray(f.limits[0]))
      writer.writerow(limitDictToArray(f.limits[1]))
      for v in f.parameters:
        writer.writerow([v.id, v.name, v.symbolType.value])
    writer.writerow(['END', "FUNCTIONS"])

# -----------------------------------------------------------------------------
# limitDictToArray()
#
# Utility function used by export
# -----------------------------------------------------------------------------

def limitDictToArray(limit):
  return [limit[Type.BOOL], limit[Type.INT], limit[Type.FLOAT], limit[Type.CHAR], limit[Type.STRING]]

# -----------------------------------------------------------------------------
# __main__
#
# Control of YACC and handler of file input
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  if (len(sys.argv) > 1):
    file = sys.argv[1]
    # Open file
    try:
      if not file.endswith('.craft'):
        print "Filename must be '.craft' type"
        exit(1)
      f = open(file, 'r')
      data = f.read()
      f.close()
      if (yacc.parse(data, tracking = True) == 'OK'):
        print(dirProc);
      export(file.replace(".craft", ".crafted"))
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

