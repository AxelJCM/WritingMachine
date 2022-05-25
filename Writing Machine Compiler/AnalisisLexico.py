from ast import If
import keyword
import re
import codecs
import os
import ply.lex as lex
import ply.yacc as yacc
import sys
import time
#import pyfirmata

# diccionario de palabras reservadas
reservadas = {
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
    'ID', # para el identificador de las variables
    'EXPONENTE', # ** 
    'SUMA', # +
    'RESTA', # -
    'DIVISION', # /
    'DIV_ENTERA', # //
    'MULTI', # *
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
    'NUMERO'
] + list(set(reservadas.values())) # first turn into a set to remove duplicate BOOLEAN values
# ver video de analizador lexico en el minuto 51:32 en caso de que de problemas de reconocimiento de tokens

"""Le dice a lex como se ven los tokens definidos anteriormente"""
t_EXPONENTE = r'\*\*' # verificar que este cambio funciona. # antes: \*\*
t_SUMA = r'\+'
t_RESTA = r'\-'
t_DIV_ENTERA = r'\/\*'
t_DIVISION = r'\/'
t_MULTI = r'\*'
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
t_ignore = r' ' # verificar que funciona para espacios, saltos de linea y tabulaciones



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


def t_PRINT(t):
    r'println\!'
    t.type = 'PRINT'
    return t

def t_COMMENTARIO(t): # se identifican los comentarios
    r'\//.*'
    pass

def t_newline(t): # se identifica una nueva linea
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_NUMERO(t): # se verifica que t sea un entero
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    return t

def t_ID(t): #funcion para los identificadores (nombres de variables)
    r'[a-z][a-zA-Z0-9@_]{0,10}'
    t.type = reservadas.get(t.value,'ID')    # Check for reserved words
    if t.value == 'true':
        t.value = True
    elif t.value == 'false':
        t.value = False
    print(len(t.value))
    if(t.type == 'ID' and ((len(t.value) < 3) or (len(t.value) > 10))):
        return t_error(t)
    #print("Lexer info")
    #print(t.value)
    #print(t.type)
    return t

def t_error(t): # Si se detecta un error durante la compilacion, se imprime dicho error en la consola del ide
    global GUI ## hacer variable global para llamar esta funcion desde el ide
    GUI.println("Se ha encontrado un error léxico en la frase '{}' de la línea {}".format(t.value, t.lexer.lineno)) # esto es lo que se tiene que imprimir en el ide en caso de error
# verificar que se recorre todo el codigo encontrando todos los errores lexicos que existan

lexer = lex.lex() # Se llama al analizador lexico


# se generan todos los tokens del codigo fuente y se imprimen
def GenerarTok(cadena):
    lexer.lineno = 0
    lexer.input(cadena)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        
cad = "mario@_ = 1"     
GenerarTok(cad)