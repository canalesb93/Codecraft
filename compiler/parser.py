# -----------------------------------------------------------------------------
# parser.py
#
# Utilizes lexer for parsing BNF rules
# -----------------------------------------------------------------------------

import sys
import ply.lex as lex
import scanner

# Classes
from symbols import SymbolTable

if sys.version_info[0] >= 3:
    raw_input = input

# Build the lexer
tokens = scanner.tokens
lex.lex(module=scanner)


precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', '<', '>', 'LESS_EQ', 'GREATER_EQ', 'EQ'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

# Program Data
global_symbol_table = SymbolTable()
current_scope = global_symbol_table

# ====== GRAMMAR ======

def p_program(p):
    'program : CRAFT "{" vars block functions "}"'
    pass

def p_vars(p):
    '''vars : var vars
            | empty'''
    pass

def p_functions(p):
    '''functions : function functions
                 | empty'''
    pass

def p_var(p):
    '''var : VAR type assignment
           | VAR type "[" NUMBER "]" assignment_array
           '''
    if p[3] != "[":
        p[3].type = p[2]
    print p[3]

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOL
            | STRING'''
    if p[1] == "int":
        p[0] = 0
    elif p[1] == "float":
        p[0] = 1
    elif p[1] == "char":
        p[0] = 2
    elif p[1] == "bool":
        p[0] = 3
    elif p[1] == "string":
        p[0] = 4
    pass

def p_assignment(p):
    '''assignment : ID "=" expression ',' assignment
                  | ID "=" expression 
                  | ID
                  '''
    var = current_scope.insert(p[1])
    if len(p) >= 4:
        var.value = p[3]
    p[0] = var
    pass

def p_assignment_array(p):
    '''assignment_array : ID "=" "{" parameters "}" ',' assignment
                        | ID "=" "{" parameters "}" 
                        | ID
                        '''
    print(p[4])
    pass

def p_function(p):
    ''' function : FUNCTION type ID "(" ")" "{" vars block "}"
                 | FUNCTION type ID "(" parameters_definition ")" "{" vars block "}"
                 | FUNCTION VOID ID "(" ")" "{" vars block "}"
                 | FUNCTION VOID ID "(" parameters_definition ")" "{" vars block "}"'''
    pass

def p_parameters(p):
    '''parameters : expression
                  | expression "," parameters'''
    if len(p) == 4:
        p[3].insert(0, p[1])
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_parameters_definition(p):
    '''parameters_definition : type
                             | type "," parameters_definition'''
    pass

def p_block(p):
    '''block : assignment block
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

# def p_statement_assign(p):
#     'statement : ID "=" expression'
#     names[p[1]] = p[3]


# def p_statement_expr(p):
#     'statement : expression'
#     print(p[1])

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
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == 'and':
        p[0] = p[1] and p[3]
    elif p[2] == 'or':
        p[0] = p[1] or p[3]

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

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('craft > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
