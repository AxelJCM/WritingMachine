import ply.lex as lex

# diccionario de palabras reservadas
reservadas = {
    'fin'    : 'FIN',
    'para'   : 'PARA',
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
    'printLine'   : 'PRINTLINE',
    'Delay'  : 'DELAY'
}  

# Lista de tokens 
"""Define los tokens validos para el lexer"""
tokens = [
    'VAR',
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
] + list(set(reservadas.values()))# first turn into a set to remove duplicate BOOLEAN values
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

# se identifican los comentarios
def t_COMMENTARIO(t): 
    r'\//.*'
    pass

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
    r'[a-z][a-zA-Z0-9_@]{3,10}'
    return t

#funcion para los identificadores 
def t_ID(t): 
    r'[A-Za-z][a-zA-Z]*'
 # Se busca en las palabras resevadas
    # Si el valor de la variable es booleana
    if t.value.upper() in reservadas: 
        t.value = t.value.upper()
        t.type = t.value
    if t.value == 'true':
        t.value = True
    elif t.value == 'false':
        t.value = False
    # Se verifica que el numero de caracterees en el nombre de las variables esté entre 3 y 10
    return t

def t_error(t): # Si se detecta un error durante la compilacion, se imprime dicho error en la consola del ide
    #global GUI ## hacer variable global para llamar esta funcion desde el ide
    #GUI.println("Se ha encontrado un error léxico en la frase '{}' de la línea {}".format(t.value, t.lexer.lineno)) # esto es lo que se tiene que imprimir en el ide en caso de error
    # verificar que se recorre todo el codigo encontrando todos los errores lexicos que existan
    print("Se ha encontrado un error léxico en la frase '{}' de la línea {}".format(t.value, t.lexer.lineno))

lexer = lex.lex() # Se crea un objeto de tipo analizador lexico para realizar el analisis


# se generan todos los tokens del codigo fuente y se imprimen
def GenerarTok(cadena):
    lexer.lineno = 0
    lexer.input(cadena)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Prueba para verificar que se identifican todos los tokens e identificadores        
cad = "(hola = true, yes = 2, IF)"    # las palabras reservadas se reconocen todas con su primera letra en minúscula 
GenerarTok(cad)