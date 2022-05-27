import ply.lex as lex
import ply.yacc as yacc
import sys
import time
#import pyfirmata


reserved = {
    'let'	 : 'LET',
    'while'	 : 'WHILE',
    'for'	 : 'FOR',
    'if'	 : 'IF',
    'else'	 : 'ELSE',
    'in'	 : 'IN',
    'OPERA'	 : 'OPERA',
    'true'	 : 'BOOLEAN',
    'false'	 : 'BOOLEAN',
    'boolean': 'BOOLEAN_TXT',
    'integer': 'INTEGER_TXT',
    'fn'     : 'FUNCTION',
    'return' : 'RETURN',
    'Move'   : 'MOVE',
    'Def'   : 'DEF',
    'Put'   : 'PUT',
    'Add'   : 'ADD',
    'ContinueUp'   : 'CONTINUEUP',
    'ContinueDown'   : 'CONTINUEDOWN',
    'ContinueRight'   : 'CONTINUERIGHT',
    'ContinueLeft'   : 'CONTINUELEFT',
    'Pos'   : 'POS',
    'PosX'   : 'POSX',
    'PosY'   : 'POSY',
    'UseColor'   : 'USECOLOR',
    'Down'   : 'DOWN',
    'Up'   : 'UP',
    'Beginning'   : 'BEGINNING',
    'Speed'   : 'SPEED',
    'Run'   : 'RUN',
    'Repeat'   : 'REPEAT',
    'If'   : 'IF',
    'IfElse'   : 'IFELSE',
    'Until'   : 'UNTIL',
    'While'   : 'WHILE',
    'Equal'   : 'EQUAL',
    'And'   : 'AND',
    'Or'   : 'OR',
    'Greater'   : 'GREATER',
    'Smaller'   : 'SMALLER',
    'Substr'   : 'SUBSTR',
    'Random'   : 'RANDOM',
    'Mult'   : 'MULT',
    'Div'   : 'DIV',
    'Sum'   : 'SUM',
    'PrintLine'   : 'PRINTLINE',
    'Delay'  : 'DELAY'
}
            
"""Define los tokens validos para el lexer"""
tokens = [
    'INT',
    'EXP',
    'THUMB',
    'INDEX',
    'MIDDLE',
    'ANULAR',
    'PINKY',
    'SEG',
    'MIL',
    'MIN',
    'ALL',
    'ARROW',
    'PRINT',
    'STR',
    'VARIABLE',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'INT_DIV',
    'OPEN_P',
    'CLOSE_P',
    'SB1',
    'SB2',
    'SQ1',
    'SQ2',
    'COMMA',
    'EQUALS_EQUALS',
    'DISTINCT',
    'LESS_EQUAL',
    'MORE_EQUAL',
    'MORE_THAN',
    'LESS_THAN',
    'PyC',
    'dDOT_E',
    'dDOT'
] + list(set(reserved.values())) # first turn into a set to remove duplicate BOOLEAN values
"""Le dice a lex como se ven los tokens definidos anteriormente"""

t_PLUS = r'\+'
t_ARROW = r'\->'
t_MINUS = r'\-'
t_INT_DIV = r'\//'
t_DIVIDE = r'\/'
t_EXP = r'\*\*'
t_MULTIPLY = r'\*'
t_EQUALS_EQUALS = r'\=='
t_EQUALS = r'\='
t_OPEN_P = r'\('
t_CLOSE_P = r'\)'
t_COMMA = r'\,'
t_DISTINCT = r'\<>'
t_LESS_EQUAL = r'\<='
t_LESS_THAN = r'\<'
t_MORE_EQUAL = r'\>='
t_MORE_THAN = r'\>'
t_PyC = r'\;'
t_dDOT_E = r'\.\.\='
t_dDOT = r'\.\.'

t_ignore = r' '

