# ![Codecraft](https://raw.githubusercontent.com/canalesb93/Codecraft/master/proposal/codecraft.png)

## Proposal Document
https://docs.google.com/document/d/13wp2fx8Qr-E8C4QgYowqk0E-wXFWvfjE1Dwm_tgwj74/edit?usp=sharing

## Grammar
```
PROGRAM ::= (VAR | BLOCK | FUNCTION)
VAR ::= 'var' TYPE ASSIGNMENT
TYPE ::= ('int' | 'float' | 'char' | 'bool' | 'string')
ASSIGNMENT ::= ('id' '=' EXPRESSION | 'id') (',' ASSIGNMENT)?
EXPRESSION ::= EXP (('<' | '>' | '<=' | '>=' | '!=') EXPRESSION)?
EXP ::= TERM (( '+' | '-') EXP)?
TERM ::= FACTOR (('*' | '/' | '%') TERM)?
FACTOR ::= ( '(' CONDITION ')' | FUNCTION_CALL | VAR_CTE )
CONDITION ::= EXPRESSION (('and' | 'or') CONDITION)?
FUNCTION ::= (TYPE | 'void') 'id' '(' PARAMETERS_DEFINITION? ')' '{' (VAR)* BLOCK '}'
PARAMETERS ::= EXPRESSION (',' PARAMETERS)?
PARAMETERS_DEFINITION ::= TYPE (',' PARAMETERS_DEFINITION)?
BLOCK ::= (ASSIGNMENT | IF | CYCLE | RETURN | BREAK | CONTINUE | FUNCTION_CALL | COMMENT)*
IF ::= 'if' '(' CONDITION ')' '{' BLOCK '}' (ELSE)?
ELSE ::= 'else' ( IF | '{' BLOCK '}' )
CYCLE ::= 'while' '(' CONDITION ')' '{' BLOCK '}'
RETURN ::= 'return' EXP?
BREAK ::= 'break'
CONTINUE ::= 'continue'
FUNCTION_CALL ::= ('id' | PREDEFINED_FUNCTIONS) '(' PARAMETERS ')'
PREDEFINED_FUNCTIONS ::= ('input' | 'output')
COMMENT ::= '/*' 'comment' '*/'
```
