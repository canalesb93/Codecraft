# -----------------------------------------------------------------------------
# scanner.py
#
# Author: Ricardo Canales and Gabriel Berlanga
#
# The module contains lexical rules used by the parser.
# -----------------------------------------------------------------------------

reserved = {
    # Basic tokens
    'craft' : 'CRAFT',
    'var' : 'VAR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'and' : 'AND',
    'or' : 'OR',
    'input' : 'INPUT',
    'output' : 'OUTPUT',
    'outputln' : 'OUTPUTLN',
    
    # Functions tokens
    'return' : 'RETURN',
    'function' : 'FUNCTION',
    'void' : 'VOID',

    # Conditional tokens
    'if' : 'IF',
    'else' : 'ELSE',

    # Cycle tokens
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',

    # Primitive types
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'bool' : 'BOOL',
    'string' : 'STRING'
}

tokens = [
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_CHAR',
    'CTE_STRING',
    'ID',
    'EQ',
    'UNEQ',
    'LESS_EQ',
    'GREATER_EQ'
] + list(reserved.values())

# Regular expressions for tokens
t_EQ  = r'=='
t_UNEQ  = r'!='
t_GREATER_EQ  = r'>='
t_LESS_EQ  = r'<='
t_CTE_INT = r'\d+'
t_CTE_FLOAT = r'[-+]?[0-9]+\.[0-9]+([Ee][\+-]?[0-9+])?'
t_CTE_CHAR = r'\'(?:\\.|[^\'\\])\''
t_CTE_STRING = r'\"((?:\\.|[^"\\])*)\"'

# Literals 
literals = [ '+','-','*','/', '%','=','(',')','{','}','[',']','<','>', ',']

# Regular expressions with action code

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignored characters (spaces and tabs)
t_ignore = " \t"

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
