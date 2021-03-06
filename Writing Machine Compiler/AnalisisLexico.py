
import re
import ply.lex as lex

error = []

# diccionario de palabras reservadas
reservadas = {
    'Beginning' : 'BEGINNING',
    'Start'  : 'START',
    'Add'    : 'ADD',
    'Def'    : 'DEF',
    'Fin'    : 'FIN',
    'Para'   : 'PARA',
    'While'	 : 'WHILE',
    'If'	 : 'IF',
    'EndIf'  : 'ENDIF',
    'Put'   : 'PUT',
    'Add'   : 'ADD',
    'ContinueUp'   : 'CONTINUEUP',
    'ContinueDown' : 'CONTINUEDOWN',
    'ContinueRight'   : 'CONTINUERIGHT',
    'ContinueLeft'   : 'CONTINUELEFT',
    'Pos'   : 'POS',
    'PosX'   : 'POSX',
    'PosY'   : 'POSY',
    'UseColor'   : 'USECOLOR',
    'Down'   : 'DOWN',
    'Up'   : 'UP',
    'Speed'   : 'SPEED',
    'Run'   : 'RUN',
    'Repeat'   : 'REPEAT',
    'IfElse'   : 'IFELSE',
    'Until'   : 'UNTIL',
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
    'Substr' : 'SUBSTR',
    'Main' : 'MAIN',
    'True' : 'TRUE',
    'False' : 'FALSE',
    'Diag' : 'DIAG' 
}  

# Lista de tokens 
"""Define los tokens validos para el lexer"""
tokens = [
    'VAR',
    'ID', # para el identificador de las variables
    'ABRE_P', # (
    'CIERRA_P', # )
    'BRACKET1', # [
    'BRACKET2', # ]
    'COMA', # ,
    'PUNTOCOMA', # ;
    'IGUAL', # =
    'DIVISION', # /
    'SUMA', # +
    'RESTA', # -
    'MULTI', # *
    'IGUAL_IGUAL', # ==
    'NUMERO', # 0...9
    'COMMENT',
    'STRING', 
] + list(reservadas.values())   # first turn into a set to remove duplicate BOOLEAN values
# ver video de analizador lexico en el minuto 51:32 en caso de que de problemas de reconocimiento de tokens

"""Le dice a lex como se ven los tokens definidos anteriormente"""
t_IGUAL = r'\=' # token de asignacion
t_DIVISION = r'\/'
t_MULTI = r'\*'
t_SUMA = r'\+'
t_RESTA = r'\-'
t_IGUAL_IGUAL = r'\=='
t_ABRE_P = r'\('
t_CIERRA_P = r'\)'
t_BRACKET1 = r'\['
t_BRACKET2 = r'\]'
t_COMA = r'\,'
t_PUNTOCOMA = r'\;'
t_ignore = '  \t' # verificar que funciona para espacios, saltos de linea y tabulaciones



"""Definicion de algunos tokens como funciones(nota: definir palabras especificas antes de la definicion de variable)"""



def t_STRING(t):
    r'["][A-Za-z ,._]+["]'
    t.value = str(t.value)
    return t

# se identifican los comentarios
def t_COMMENT(t):
    r'\//.*'
    t.value = str(t.value) + str(t.lexer.lineno)
    return t

def t_PARA(t):
    r'Para'
    t.value = "PARA"
    t.type = t.value
    return t

def t_FIN(t):
    r'Fin'
    t.value = "FIN"
    t.type = t.value
    return t

def t_ENDIF(t):
    r'EndIf'
    t.value = "ENDIF"
    t.type = t.value
    return t



# se identifica una nueva linea
def t_newline(t): 
    r'\n+' 
    t.lexer.lineno += len(t.value)

# se verifica que t sea un entero
def t_NUMERO(t): 
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    return t

def t_VAR(t):
    r'[a-z][a-zA-Z0-9@_]*'
    if 10 < len(t.value) < 3 or t.value[0].isupper():
        return t_error(t)
    return t

#funcion para los identificadores 
def t_ID(t): 
    r'[A-Z][a-zA-Z0-9@_]*' #r'[A-Za-z][a-zA-Z@_]*'
    t.type = reservadas.get(t.value,'ID')    # Se busca en las palabras resevadas
    if t.value.upper() in reservadas: 
        t.value = t.value.upper()
        t.type = t.value
    return t

def t_error(t): # Si se detecta un error durante la compilacion, se imprime dicho error en la consola del ide
    if t is not None:
        error.append("Se ha encontrado un error lexico en la frase '{}' de la linea {}".format(t.value, t.lexer.lineno))
    else:
        pass

    print("error:")
    print(error)
    #GUI.println("Se ha encontrado un error l??xico en la frase '{}' de la l??nea {}".format(t.value, t.lexer.lineno)) # esto es lo que se tiene que imprimir en el ide en caso de error
    # verificar que se recorre todo el codigo encontrando todos los errores lexicos que existan
    #print(error)

lexer = lex.lex() # Se crea un objeto de tipo analizador lexico para realizar el analisis


# se generan todos los tokens del codigo fuente y se imprimen
def lexicalAnalizer(cadena):
    lexer.lineno = 0
    lexer.input(cadena)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Prueba para verificar que se identifican todos los tokens e identificadores        
#cad = "Def a6578 \t sdfd \n , 3;"    # las palabras reservadas se reconocen todas con su primera letra en min??scula 
#LexicalAnalizer(cad)
def lex_getErrores():
    return error  

# Funcion para limpiar los valores de la lista de errores
def limpiarError():
    error.clear()