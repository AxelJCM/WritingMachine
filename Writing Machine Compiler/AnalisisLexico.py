from ast import If
import ply.lex as lex
import ply.yacc as yacc
import sys
import time
#import pyfirmata

# diccionario de palabras reservadas
reserved = {
    'for'	         : 'FOR',
    'true'	         : 'BOOLEAN',
    'false'	         : 'BOOLEAN',
    'return'         : 'RETURN',
    'Delay'          : 'DELAY',
    'Def'            : 'DEF',
    'Put'            : 'PUT',
    'Add'            : 'ADD',
    'ContinueUp'     : 'CONTINUEUP',
    'ContinueDown'   : 'CONTINUEDOWN',
    'ContinueRight'  : 'CONTINUERIGHT',
    'ContinueLeft'   : 'CONTINUELEFT',
    'Pos'            : 'POS',
    'PosX'           : 'POSX',
    'PosY'           : 'POSY',
    'UseColor'       : 'USECOLOR',
    'Down'           : 'DOWN',
    'Up'             : 'UP',
    'Beginning'      : 'BEGINNING',
    'Speed'          : 'SPEED',
    'Run'            : 'RUN',
    'Repeat'         : 'REPEAT',
    'If'             : 'IF',
    'IfElse'         : 'IFELSE',
    'Until'          : 'UNTIL',
    'While'          : 'WHILE',
    'Equal'          : 'EQUAL',
    'And'            : 'AND',
    'Or'             : 'OR',
    'Greater'        : 'GREATER',
    'Smaller'        : 'SMALLER',
    'Substr'         : 'SUBSTR',
    'Random'         : 'RANDOM',
    'Mult'           : 'MULT',
    'Div'            : 'DIV',
    'Sum'            : 'SUM',
    'PrintLine'      : 'PRINTLINE'
}     

# Lista de tokens 
"""Define los tokens validos para el lexer"""
tokens = [
    'EXPONENTE', # **
    'IMPRIMIR', # impresion    
    'SUMA', # +
    'RESTA', # -
    'DIVISION', # /
    'DIV_ENTERA', # //
    'MULT', # *
    'IGUAL', # =
    'ABRE_P', # (
    'CIERRA_P', # )
    'BRACKET1', # [
    'BRACKET2', # ]
    'COMA', # ,
    'PUNTO_COMA', # ;
    'IGUAL_IGUAL', # ==
    'DIFERENTE', # !=
    'NEGACION', # !
    'MENOR_IGUAL', # <=
    'MAYOR_IGUAL', # >=
    'MAYOR_QUE', # >
    'MENOR_QUE', # <
    'dDOT_E', #
    'dDOT', #
] + list(set(reserved.values())) # first turn into a set to remove duplicate BOOLEAN values

"""Le dice a lex como se ven los tokens definidos anteriormente"""
t_EXPONENETE = r'\*\*'
t_SUMA = r'\+'
t_RESTA = r'\-'
t_DIV_ENTERA = r'\//'
t_DIVISION = r'\/'
t_MULT = r'\*'
t_IGUAL_IGUAL = r'\=='
t_IGUAL = r'\='
t_ABRE_P = r'\('
t_CIERRA_P = r'\)'
t_BRACKET1 = r'\['
t_BRACKET2 = r'\]'
t_COMA = r'\,'
t_PUNTO_COMA = r'\;'
t_DIFERENTE = r'\!='
t_NEGACION = r'\!'
t_MENOR_IGUAL = r'\<='
t_MENOR_QUE = r'\<'
t_MAYOR_IGUAL = r'\>='
t_MAYOR_QUE = r'\>'
t_dDOT_E = r'\.\.\='
t_dDOT = r'\.\.'

t_IF = r'If'
t_IFELSE = r'IfElse'
t_FOR = r'For'
t_RETURN = r'return'
t_DELAY = r'delay'
t_DEF = r'Def'
t_PUT = r'Put'
t_ADD = r'Add'
t_CONTINUEUP = r'ContinueUp'
t_CONTINUEDOWN = r'ContinueDown'
t_CONTINUERIGHT = r'ContinueRight'
t_CONTINUELEFT = r'ContinueLeft'
t_POS = r'Pos'
t_POSX = r'PosX'
t_POSY = r'PosY'
t_USECOLOR = r'UseColor'
t_DOWN = r'Down'
t_UP = r'Up'
t_BEGINNING = r'Beginnig'
t_SPEED = r'Speed'
t_RUN = r'Run'
t_REPEAT = r'Repeat'
t_IF = r'If'
t_IFELSE = r'IfElse'
t_UNTIL = r'Until'
t_WHILE = r'While'
t_EQUAL = r'Equal'
t_AND = r'And'
t_OR = r'Or'
t_GREATER = r'Greater'
t_SMALLER = r'Smaller'
t_SUBSTR = r'Substr'
t_RANDOM = r'Random'
t_MULT = r'Mult'
t_DIV = r'Div'
t_SUM = r'Sum'
t_PRINTLINE = r'PrintLine'




t_ignore = r'\t\n'

"""Definicion de algunos tokens como funciones(nota: definir palabras especificas antes de la definicion de variable)"""

############################## Esta vara se usa cuando se escribe el codigo #############################
# board = pyfirmata.Arduino('COM3')
#
# it = pyfirmata.util.Iterator(board)
# it.start()
# angle = 0
#
# pin3 = board.get_pin('d:3:s')
# pin5 = board.get_pin('d:5:s')
# pin6 = board.get_pin('d:6:s')
# pin9 = board.get_pin('d:9:s')
# pin10 = board.get_pin('d:10:s')
#
# pin3.write(angle)
# pin5.write(angle)
# pin6.write(angle)
# pin9.write(angle)
# pin10.write(angle)
########################################################################################################


def t_THUMB(t): # para pulgar 
    r'\"P\"'
    t.type = 'THUMB'
    return t
def t_INDEX(t): # para dedo indice
    r'\"I\"'
    t.type = 'INDEX'
    return t
def t_MIDDLE(t): # para dedo medio
    r'\"M\"'
    t.type = 'MIDDLE'
    return t
def t_ANULAR(t): # para dedo anular
    r'\"A\"'
    t.type = 'ANULAR'
    return t
def t_PINKY(t): # para dedo meñique
    r'\"Q\"'
    t.type = 'PINKY'
    return t

def t_ALL(t): # supongo que ALL son todos lo dedos
    r'\"T\"'
    t.type = 'ALL'
    return t

def t_SEG(t):
    r'\"Seg\"'
    t.value = "Seg"
    t.type = 'SEG'
    return t
def t_PRINT(t):
    r'println\!'
    t.type = 'PRINT'
    return t

def t_MIL(t):
    r'\"Mil\"'
    t.value = "Mil"
    t.type = 'MIL'
    return t

def t_MIN(t):
    r'\"Min\"'
    t.value = "Min"
    t.type = 'MIN'
    return t

def t_STR(t):
    r"\"[a-zA-Z ]+\""
    t.value = t.value[1:-1]
    t.type = 'STR'
    return t

def t_COMMENT(t): # se identifican los comentarios
    r'\@.*'
    pass

def t_newline(t): # se identifica una nueva linea
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_INT(t): # se verifica que t sea un entero
    r'\d+'
    t.value = int(t.value)
    return t

def t_SB1(t):
    r'\{'
    t.type = 'SB1'
    return t

def t_SB2(t):
    r'\}'
    t.type = 'SB2'
    return t

def t_SQ1(t): # verifica si es un parentesis cuadrado
    r'\['
    t.type = 'SQ1'
    return t

def t_SQ2(t):
    r'\]'
    t.type = 'SQ2'
    return t

def t_ID(t):
    r'[a-zA-Z#_?][a-zA-Z0-9#_?]{0,14}'
    t.type = reserved.get(t.value,'VARIABLE')    # Se busca t en el diccionario de palabras reservadas
    if t.value == 'true':
        t.value = True
    elif t.value == 'false':
        t.value = False
    if(t.type == 'VARIABLE' and len(t.value) < 3):
        return t_error(t)
    #print("Lexer info")
    #print(t.value)
    #print(t.type)
    return t

def t_error(t): # Si se detecta un error durante la compilacion, se imprime dicho error en la consola del ide
    global GUI
    GUI.println("Frase ilegal '{}' en línea {}".format(t.value, t.lexer.lineno))

lexer = lex.lex() # Se llama al analizador lexico