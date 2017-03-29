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

if sys.version_info[0] >= 3:
    raw_input = input

# =============== Lexer SETUP ===============
tokens = scanner.tokens
lex.lex(module=scanner)

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', '<', '>', 'LESS_EQ', 'GREATER_EQ', 'EQ'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS'),
)

# =============== Lexer END ===============

# =============== Global START ===============

'''
Prepend "__" to all global variables for easy undestanding.
Remember to use "global" when modifying these variables in 
a different scope.
''' 

# Symbol Tables
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
    pass

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
    '''var_repeater : "," ID addVariable var_array var_assignment var_repeater
                    | empty
                    '''

def p_var_assignment(p):
    '''var_assignment : "=" expression
                      | empty
                      '''

def p_var_array(p):
    '''var_array : "[" NUMBER "]" setTypeAsArray
                 | empty'''

def p_functions(p):
    '''functions : function functions
                 | empty'''
    pass

# def p_assignment_array(p):
#     '''assignment_array : ID "=" "{" parameters "}" ',' assignment
#                         | ID "=" "{" parameters "}" 
#                         | ID
#                         '''
#     pass

def p_var_free_assignment(p):
    '''var_free_assignment : ID var_assignment'''

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
    '''parameters : expression parameters1
                  | empty'''
    pass

def p_parameters1(p):
    '''parameters1 : "," expression parameters1
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
    '''if : IF "(" expression ")" "{" block "}"
          | IF "(" expression ")" "{" block "}" else'''
    pass

def p_else(p):
    '''else : ELSE if
            | ELSE "{" block "}"'''
    pass

def p_cycle(p):
    'cycle : WHILE "(" expression ")" "{" block "}"'
    pass

def p_return(p):
    '''return : RETURN
              | RETURN expression'''
    pass

def p_function_call(p):
    '''function_call : ID "(" ")" 
                     | ID "(" parameters ")"'''
    pass

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression EQ expression
                  | expression LESS_EQ expression
                  | expression GREATER_EQ expression
                  | expression AND expression
                  | expression OR expression'''
    pass

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_boolean(p):
    '''expression : FALSE
                  | TRUE'''
    if p[1] == 'false':
        p[0] = False
    elif p[1] == 'true':
        p[0] = True

def p_expression_id(p):
    "expression : ID"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_function_call(p):
    'expression : function_call'
    pass

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
  varName = __tVarName
  addVariable(varName, __tVarType)

def p_setTypeAsArray(p):
  'setTypeAsArray :'
  setTypeAsArray()

# =============== Grammar Actions END ===============

def addVariable(name, varType):
  global __varsGlobal
  global __varsLocal
  if(varType == Type.VOID):
    print("Variable error : can't be of VOID type")
    return
  
  variable = Var(name, varType)
  if __scope == Scope.GLOBAL:
    # Construct variable globally
    __varsGlobal.insert(variable)
  elif __scope == Scope.LOCAL:
    # Construct variable locally
    __varsLocal.insert(variable)

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
  print "\nSummary:"
  print "G-VARS:", __varsGlobal
  print "L-VARS:", __varsLocal
  print "G-FUNCS:", __funcsGlobal

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

