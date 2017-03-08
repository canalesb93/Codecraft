# module: scanner.py
# This module just contains the lexing rules

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
    'NUMBER',
    'ID',
    'EQ',
    'LESS_EQ',
    'GREATER_EQ',
] + list(reserved.values())

# Regular expressions for tokens
t_EQ  = r'=='
t_GREATER_EQ  = r'>='
t_LESS_EQ  = r'<='

# Literals 
literals = [ '+','-','*','/', '%','=','(',')','{','}','[',']','<','>', ',' ]

# Regular expressions with action code

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

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
