import ply.yacc as yacc
import os
import codecs
import re
from AnalisisLexico import *
#from AnalisisSemantico import runSemanticAnalizer
from sys import stdin
from pip._vendor.distlib.compat import raw_input
import random

contproc = 0
global contmain
contmain = 0

precedence = (
    ('right', 'PUNTOCOMA'),
    ('left', 'BRACKET2'),
    ('right', 'BRACKET1'),
    ('right', 'IGUAL_IGUAL', 'IGUAL', 'NEGACION'), 
    ('right', 'COMA'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'SMALLER', 'GREATER'),
    ('left', 'DIVISION', 'MULTI'),
    ('left', 'CIERRA_P'),
    ('right', 'ABRE_P'), 
)


# Define las listas necesarias
ids = {}

nombres = {}

arduino = []

prints = []

errores = []

# Funciones para el arbol

def p_Start(p):
    '''
    Start : COMMENT cuerpo
    '''
    if p[1] == '$':
        p_error
    else:
        p[0] = p[2]
    

def p_cuerpo(p):
    '''
    cuerpo : variable
           | procedimiento
           | main
           | COMMENT cuerpo
           | Put
           | Put2
            '''
    global contproc
    global contmain
    if p[1] == '\//.*':
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]
        
def p_cuerpo2(p):
    '''
    cuerpo2 : variablexd
            | COMMENT cuerpo2
            | expresion
            | llamadoproc
            | empty
            | Put2
            | Put
            '''
    global contproc

    if p[1] == '\//.*':
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

def p_cuerpo3(p):
    '''
    cuerpo3 : variablexdd
            | COMMENT cuerpo3
            | expresion
            | funcion
            | empty
            | Put
            | Put2
            '''
    global contproc
    global contmain
    contmain = 0
    if p[1] == '\//.*':
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

def p_id(p):
    '''
    id : ID
    '''
    try:
        if ids[p[1]] == None:
            p[0] = p[1]
            ids[p[1]]
        else:
            p_error
    except:
        errores.append("Procedimiento ya existe")
        
def p_procedimiento(p): # no puede haber dos o mas procedimientos con el mismo nombre
    
    '''
    procedimiento : PARA id BRACKET1 empty BRACKET2 cuerpo2 FIN cuerpo
                  | PARA id BRACKET1 parametro BRACKET2 cuerpo2 FIN cuerpo
    '''
    
    global contproc
    if p[8] != '$':
        p[0] = (p[2], p[4], p[6],p[8])
    else:   
        p[0] = (p[2], p[4],p[6])
    ids[p[2]] = (p[4],p[6])
    print(ids)
        
def p_llamadoproc(p):
    '''
    llamadoproc : PARA id BRACKET1 parametro BRACKET2 PUNTOCOMA
    '''
                
def p_main(p):
    '''
    main : MAIN BRACKET1 BRACKET2 cuerpo3 FIN cuerpo
    '''
    global contmain
    global contproc
    print("dawdwa")
    print(contmain)
    if contmain == 0:
        contmain = 1
        if p[6] != '$':
            p[0] = (p[4],p[6])
        else:
            p[0] = (p[4])
    else:
        contmain = 0
        errores.append("errorazo")

def p_Variable(p):
    '''
    variable : variable1 cuerpo
            | variable2 cuerpo
            | empty empty
    '''
    if (p[2] != '$'):
        p[0] = (p[1])
    else:
        p[0] = (p[1],p[2])
    
def p_Variablexd(p):
    '''
    variablexd : variable1 cuerpo2
            | variable2 cuerpo2
            | empty empty
    '''
    if (p[2] != '$'):
        p[0] = (p[1])
    else:
        p[0] = (p[1],p[2])
        
def p_Variablexdd(p):
    '''
    variablexdd : variable1 cuerpo3
            | variable2 cuerpo3
            | empty empty
    '''
    if (p[2] != '$'):
        p[0] = (p[1])
    else:
        p[0] = (p[1],p[2])


def p_Variable1(p):
    '''
    variable1 : DEF VAR PUNTOCOMA
    '''
    p[0] = (p[1], p[2])
    print(p[1], p[2])


def p_Variable2(p):
    '''
    variable2 : DEF VAR IGUAL NUMERO PUNTOCOMA
    '''
    print(p[2])
    print(p[4])
    nombres[p[2]] = p[4]
    p[0] = (p[1], p[2], p[3], p[4])
    print(p[2], p[3], p[4])
    print(nombres)



def p_expresion(p):
    '''
    expresion : funcion expresion
              | expresion_alge1 expresion
              | expresion_alge2 expresion
              | Sum expresion
              | Substr expresion
              | Mult expresion
              | Div expresion
              | funcion empty
              | expresion_alge1 empty
              | expresion_alge2 empty
              | Sum empty
              | Substr empty
              | Mult empty
              | Div empty
              | empty empty
                        
    '''

    if (p[2] != '$'):
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]
        
def p_orden(p):
    '''
    ordenes : Beginning empty
            | ContinueUp empty
            | ContinueDown empty
            | ContinueRight empty
            | ContinueLeft empty
            | Up empty
            | Down empty
            | Speed empty
            | Pos empty
            | PosX empty
            | PosY empty
            | UseColor empty
            | PUNTOCOMA ordenes
            | empty empty
    '''
    if p[2] != '$':
            p[0] = p[1]
    else:
        p[0] = (p[1],p[2])
        
def p_funcion(p):
    '''
    funcion : Random empty
            | Run empty
            | If empty
            | IfElse empty
            | Repeat empty
            | Until empty
            | While empty
            | PrintLine empty
            | And empty
            | Or empty
            | Add empty
            | Put2 empty 
            | Put empty
            | PUNTOCOMA funcion
            | empty empty
         
       
    '''
    if p[2] != '$':
        p[0] = p[1]
    else:
        p[0] = (p[1],p[2])


def p_Put(p): # se puede mejorar con "expresion" Tambien puede sumarse una 
    # variable numerica o uno de tipo "funcion"
    '''
    Put : PUT ABRE_P VAR COMA VAR CIERRA_P PUNTOCOMA
    '''
    try:
        if (nombres[p[3]] != "$") and (nombres[p[5]] != "$"):
            nombres[p[3]] = nombres[p[5]]
            p[0] = (p[1], p[3], p[5])
    except:
        errores.append("Variable no declarada")
        
def p_Put2(p): # se puede mejorar con "expresion" Tambien puede sumarse una 
    # variable numerica o uno de tipo "funcion"
    '''
    Put2 : PUT ABRE_P VAR COMA NUMERO CIERRA_P PUNTOCOMA
        | PUT ABRE_P VAR COMA expresion_alge1 CIERRA_P PUNTOCOMA
        | PUT ABRE_P VAR COMA expresion_alge2 CIERRA_P PUNTOCOMA
        | PUT ABRE_P VAR COMA funcion CIERRA_P PUNTOCOMA
    '''
    if (nombres[p[3]] != "$"):
        nombres[p[3]] = p[5]
        p[0] = (p[1], p[3], p[5])
    else:
        p_error
        
def p_condicion(p):
    '''
    condicion : Equal
              | Greater
              | Smaller
    '''
    p[0] = p[1]    
    
def expresion_alge(p):
    '''
    expresion_alge : expresion_alge1
                   | expresion_alge2
                   
    '''
    p[0] = p[1]

def p_expresion_alge1(p):

    '''
    expresion_alge1 : NUMERO SUMA NUMERO 
                   | NUMERO RESTA NUMERO 
                   | NUMERO MULTI NUMERO 
                   | NUMERO DIVISION NUMERO
                   | NUMERO EXPONENTE NUMERO
    '''

    if p[2] == '+' : p[0] = p[1]+p[3]
    elif p[2] == '-' : p[0] = p[1]-p[3]
    elif p[2] == '*' : p[0] = p[1]*p[3]
    elif p[2] == '/' : p[0] = p[1]/p[3]
    elif p[2] == '^' : p[0] = p[1]**p[3]

    print(p[0])

def p_expresion_alge2(p):

    '''
    expresion_alge2 : ABRE_P expresion_alge1 CIERRA_P SUMA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P RESTA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P MULT ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P DIV ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P EXPONENTE ABRE_P expresion_alge1 CIERRA_P
                   
    '''

    if p[4] == '+' : p[0] = p[2]+p[6]
    elif p[4] == '-' : p[0] = p[2]-p[6]
    elif p[4] == '*' : p[0] = p[2]*p[6]
    elif p[4] == '/' : p[0] = p[2]/p[6]
    elif p[4] == '^' : p[0] = p[2]**p[6]
    

def p_Sum(p):
    '''
    Sum : SUM ABRE_P NUMERO COMA NUMERO CIERRA_P
           | SUM ABRE_P NUMERO COMA expresion_alge1 CIERRA_P
           | SUM ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
           | SUM ABRE_P NUMERO COMA Var CIERRA_P
           | SUM ABRE_P Var COMA NUMERO CIERRA_P
           | SUM ABRE_P Var COMA Var CIERRA_P
           | SUM ABRE_P expresion_alge1 COMA Var CIERRA_P
           | SUM ABRE_P expresion_alge1 COMA NUMERO CIERRA_P
           | SUM ABRE_P Var COMA expresion_alge1 CIERRA_P
    '''

    p[0] = int(p[3]) + int(p[5])


def p_Substr(p):
    '''
    Substr : SUBSTR ABRE_P NUMERO COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P NUMERO COMA expresion_alge1 CIERRA_P
           | SUBSTR ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
           | SUBSTR ABRE_P NUMERO COMA Var CIERRA_P
           | SUBSTR ABRE_P Var COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P Var COMA Var CIERRA_P
           | SUBSTR ABRE_P expresion_alge1 COMA Var CIERRA_P
           | SUBSTR ABRE_P expresion_alge1 COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P Var COMA expresion_alge1 CIERRA_P
    '''

    p[0] = int(p[3]) - int(p[5])

def p_Mult(p):
    '''
    Mult : MULTI ABRE_P NUMERO COMA NUMERO CIERRA_P
           | MULTI ABRE_P NUMERO COMA expresion_alge1 CIERRA_P
           | MULTI ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
           | MULTI ABRE_P NUMERO COMA Var CIERRA_P
           | MULTI ABRE_P Var COMA NUMERO CIERRA_P
           | MULTI ABRE_P Var COMA Var CIERRA_P
           | MULTI ABRE_P expresion_alge1 COMA Var CIERRA_P
           | MULTI ABRE_P expresion_alge1 COMA NUMERO CIERRA_P
           | MULTI ABRE_P Var COMA expresion_alge1 CIERRA_P
    '''

    p[0] = int(p[3]) * int(p[5])

def p_Div(p):
    '''
    Div : DIV ABRE_P NUMERO COMA NUMERO CIERRA_P
           | DIV ABRE_P NUMERO COMA expresion_alge1 CIERRA_P
           | DIV ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
           | DIV ABRE_P NUMERO COMA Var CIERRA_P
           | DIV ABRE_P Var COMA NUMERO CIERRA_P
           | DIV ABRE_P Var COMA Var CIERRA_P
           | DIV ABRE_P expresion_alge1 COMA Var CIERRA_P
           | DIV ABRE_P expresion_alge1 COMA NUMERO CIERRA_P
           | DIV ABRE_P Var COMA expresion_alge1 CIERRA_P
    '''

    p[0] = int(p[3]) / int(p[5])

def p_var(p):
    '''
    Var : VAR
    '''
    try:
        if nombres[p[1]] != '$':
            p[0] = nombres[p[1]]
        else:
            p_error
    except:
        errores.append("Variable no declarado")
    
def p_Equal(p):
    '''
    Equal : EQUAL ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge2 COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P Var COMA Var CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P NUMERO COMA Var CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge2 COMA Var CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge1 COMA Var CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P Var COMA NUMERO CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P Var COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P Var COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge1 COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge2 COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge1 COMA NUMERO CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P expresion_alge2 COMA NUMERO CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P NUMERO COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | EQUAL ABRE_P NUMERO COMA expresion_alge2 CIERRA_P PUNTOCOMA
    '''

    if p[3] == p[5]:
        p[0] = True
    else:
        p[0] = False
        

def p_Greater(p):
    '''
    Greater : GREATER ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge2 COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P Var COMA Var CIERRA_P PUNTOCOMA
          | GREATER ABRE_P NUMERO COMA Var CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge2 COMA Var CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge1 COMA Var CIERRA_P PUNTOCOMA
          | GREATER ABRE_P Var COMA NUMERO CIERRA_P PUNTOCOMA
          | GREATER ABRE_P Var COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P Var COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge1 COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge2 COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge1 COMA NUMERO CIERRA_P PUNTOCOMA
          | GREATER ABRE_P expresion_alge2 COMA NUMERO CIERRA_P PUNTOCOMA
          | GREATER ABRE_P NUMERO COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | GREATER ABRE_P NUMERO COMA expresion_alge2 CIERRA_P PUNTOCOMA
            
    '''
    
    if p[3] > p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])


def p_Smaller(p):
    '''
    Smaller : SMALLER ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge2 COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P Var COMA Var CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P NUMERO COMA Var CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge2 COMA Var CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge1 COMA Var CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P Var COMA NUMERO CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P Var COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P Var COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge1 COMA expresion_alge2 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge2 COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge1 COMA NUMERO CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P expresion_alge2 COMA NUMERO CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P NUMERO COMA expresion_alge1 CIERRA_P PUNTOCOMA
          | SMALLER ABRE_P NUMERO COMA expresion_alge2 CIERRA_P PUNTOCOMA
    '''
    
    if p[3] < p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])



def p_And(p): # expresion tambien puede ser exp_agl1y2
    ''' And : AND ABRE_P expresion COMA expresion CIERRA_P PUNTOCOMA '''
    
    if p[3] == True and p[5] == True:
        p[0] = True
    else:
        p[0] = False




def p_Or(p): # igual que el AND
    ''' Or : OR ABRE_P expresion COMA expresion CIERRA_P PUNTOCOMA '''

    p[0] = p[2] or p[5]
    
    

def p_If(p): # en lugar de condicion tambien puede tener exp_alg1 y 2
    # funcion debe ir separado por ; (lo mismo que Run)

    '''
    If : IF ABRE_P condicion CIERRA_P BRACKET1 funcion BRACKET2 
    '''

    print(p[3])

    if(p[3]):
        p[0] = p[6]

def p_IfElse(p): # para la condicion: puede tener exp_alg1y2, puede estar o no separados por;
    # lo de funcion y los ultimos brackets: lo mismo que Run.
    '''
    IfElse : IFELSE ABRE_P condicion CIERRA_P BRACKET1 funcion BRACKET2 BRACKET1 funcion BRACKET2
    '''

    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[9]

# Mientras se cumpla la condicion, se ejecutan las funciones
def p_While(p):
    ''' 
    While : WHILE BRACKET1 condicion BRACKET2 BRACKET1 funcion BRACKET2
    
    '''
    while(p[3]):
        p[0] = p[6]

# Se repiten las funciones NUMERO cantidad de veces
def p_Repeat(p):
    ''' 
    Repeat : REPEAT NUMERO BRACKET1 ordenes BRACKET2
    '''
    for i in range(p[2]):
         p[0] = p[4]

# Se ejecutan funciones hasta que se cumpla la condicion
def p_until(p):
    ''' 
    Until : UNTIL BRACKET1 funcion BRACKET2 BRACKET1 condicion BRACKET2
    '''
    p[0] = p[3]
    while True:
        if(p[6]):
            p[0] = p[3]
        else:
            break
    
# Se suma un valor a la variable en cuestion
def p_add(p): 
    '''
    Add : ADD ABRE_P Var empty empty CIERRA_P PUNTOCOMA
        | ADD ABRE_P Var COMA NUMERO CIERRA_P PUNTOCOMA
        | ADD ABRE_P Var COMA expresion_alge1 CIERRA_P PUNTOCOMA
        | ADD ABRE_P Var COMA Var CIERRA_P PUNTOCOMA
        | ADD ABRE_P Var COMA expresion_alge2 CIERRA_P PUNTOCOMA
    '''
    if p[4] == '$':
        p[0]= p[3]+1
    else:
        p[0]= p[3]+ p[5]
    
# Producciones para parametro
def p_parametro(p):
    '''
    parametro : Var COMA parametro
              | Var empty empty
              | empty empty empty
    '''
    if p[3] != '$' and p[2] != '$':
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

# Posiciona el lapicero en la posicion (0,0)
def p_beginning(p):
    '''
    Beginning : BEGINNING PUNTOCOMA
    '''
    p[0] = p[1]
    arduino.append(['Beginning', ''])
    

# Generar un numero aleatorio comprendido  entre 0 y n.
def p_random(p):
    '''
    Random : RANDOM ABRE_P NUMERO CIERRA_P PUNTOCOMA'''
    
    p[0] = random.randrange(p[3])

# Se escribe en el liezo las unidades hacia arriba que se le indiquen 
def p_ContinueUp(p): # recibe numero, operacion aritmetica, variables
    '''
    ContinueUp : CONTINUEUP NUMERO PUNTOCOMA
               | CONTINUEUP expresion_alge1 PUNTOCOMA
               | CONTINUEUP expresion_alge2 PUNTOCOMA
               | CONTINUEUP Var PUNTOCOMA 
    '''
    p[0] = p[2]
    arduino.append(['ContineUp',p[2]])
    

# Se escribe en el liezo las unidades hacia abajo que se le indiquen 
def p_ContinueDown(p): # recibe numero, operacion aritmetica, variables
    '''
    ContinueDown : CONTINUEDOWN NUMERO PUNTOCOMA
                 | CONTINUEDOWN expresion_alge1 PUNTOCOMA
                 | CONTINUEDOWN expresion_alge2 PUNTOCOMA
                 | CONTINUEDOWN Var PUNTOCOMA 
    '''

    p[0] = p[2]
    arduino.append(['ContineDown',p[2]])


# Se escribe en el liezo las unidades hacia la derecha que se le indiquen 
def p_ContinueRight(p):
    '''
    ContinueRight : CONTINUERIGHT NUMERO PUNTOCOMA
                  | CONTINUERIGHT expresion_alge1 PUNTOCOMA
                  | CONTINUERIGHT expresion_alge2 PUNTOCOMA
                  | CONTINUERIGHT Var PUNTOCOMA 
    '''

    p[0] = p[2]
    arduino.append(['ContineRight',p[2]])

# Se escribe en el liezo las unidades hacia la izquierda que se le indiquen 
def p_ContinueLeft(p):
    '''
    ContinueLeft : CONTINUELEFT NUMERO PUNTOCOMA
                 | CONTINUELEFT expresion_alge1 PUNTOCOMA
                 | CONTINUELEFT expresion_alge2 PUNTOCOMA
                 | CONTINUELEFT Var PUNTOCOMA 
    '''

    p[0] = p[2]
    arduino.append(['ContineLeft',p[2]])

# Levanta el lapicero utilizado para que no toque el lienzo
def p_Up(p):
    '''
    Up : UP PUNTOCOMA
    '''
    p[0] = p[1]
    arduino.append(['Up', ''])

    


# Baja el lapicero utilizado hasta tocar el lienzo
def p_Down(p):
    '''
    Down : DOWN PUNTOCOMA
    '''
    p[0] = p[1]
    arduino.append(['Down', ''])

# Se define la velocidad de impresion
def p_Speed(p):
    '''
    Speed : SPEED NUMERO PUNTOCOMA
    '''
    p[0] = p[2]
    arduino.append(['Speed', p[2]])

# Posiciona el lapicero en la posicion X,Y que recibe la funcion
def p_Pos(p):
    '''
    Pos : POS ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
        | POS ABRE_P expresion_alge1 COMA NUMERO CIERRA_P PUNTOCOMA
        | POS ABRE_P NUMERO COMA expresion_alge1 CIERRA_P PUNTOCOMA
        | POS ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
        | POS ABRE_P Var COMA NUMERO CIERRA_P PUNTOCOMA
        | POS ABRE_P NUMERO COMA Var CIERRA_P PUNTOCOMA
        | POS ABRE_P Var COMA Var CIERRA_P PUNTOCOMA
        | POS ABRE_P expresion_alge1 COMA Var CIERRA_P PUNTOCOMA
        | POS ABRE_P Var COMA expresion_alge1 CIERRA_P PUNTOCOMA
    '''

    p[0] = (p[3],p[5])
    arduino.append(['Pos',[p[3],p[5]]])
    


# Posiciona el lapicero en la posicion equivalente al numero que recibe la funcion
def p_PosX(p): 
    
    '''
    PosX : POSX NUMERO PUNTOCOMA
        | POSX expresion_alge1 PUNTOCOMA
        | POSX expresion_alge2 PUNTOCOMA
        | POSX Var PUNTOCOMA
    '''

    p[0] = p[2]
    arduino.append(['PosX',p[2]])
 
# Posiciona el lapicero en la posicion equivalente al numero que recibe la funcion
def p_PosY(p): 
    
    '''
    PosY : POSY NUMERO PUNTOCOMA
        | POSY expresion_alge1 PUNTOCOMA
        | POSY expresion_alge2 PUNTOCOMA
        | POSY Var PUNTOCOMA
    '''
    p[0] = p[2] 
    arduino.append(['PosY',p[2]])

# Se verifica que el numero de color que se quiere utilizar es aceptado
def p_UseColor(p):
    
    '''
    UseColor : USECOLOR NUMERO PUNTOCOMA
            | USECOLOR Var PUNTOCOMA
            | USECOLOR empty PUNTOCOMA
    '''
    if p[2] == '$':
        p[0] = 1
    elif p[2] in range(1,2):
        p[0] = p[2]
        print("UseColor "+ str(p[2]))
    else:
        errores.append("Indice para seleccion de color fuera de rango")

    arduino.append(['UseColor',p[2]])

# corresponde al cuerpo de las instrucciones. 
def p_Run(p): 
    '''
    Run : RUN BRACKET1 ordenes BRACKET2 PUNTOCOMA
    '''
    p[0] = p[3]

def p_exp(p):
    '''
    exp : NUMERO COMA exp
        | STRING COMA exp
        | Var COMA exp
        | NUMERO empty empty
        | STRING empty empty
        | Var empty empty
    '''
    if p[2] != '$':
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

# se definen las producciones para el printLine
def p_PrintLine(p): 
    ''' PrintLine : PRINTLINE ABRE_P exp CIERRA_P PUNTOCOMA'''
    p[0] = p[3]
    prints.append(p[3])
 
# se define como se ve la produccion epsilon dentro de la gramatica
def p_empty(p):
    '''
    empty :
    '''
    p[0] = '$'

# Funcion para ir recopilando los errores que encuentre el analizador sintactico
def p_error(p):
    print("se encuentra error")
    if p is not None:
        errores.append("Error de sintaxis ({}) en linea {}".format(str(p.value), str(p.lineno)))
        print(errores)
    else:
        print(str(p.value))
        errores.append("Error de sintaxis")
        
    
# Se crea una instancia del parser   
parser = yacc.yacc()

# Funcion que inicia el analizador sintactico
def sintacticAnalizer(cadena):
    parser = yacc.yacc()
    parser.parse(cadena)

#cad = "// dadaw \n Para Axel[mario]\n Para Chris[dawdaw]\n Fin\n Fin"
#sintacticAnalizer(cad)

#################################### tester ############################################

def buscarFichero(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1
    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)
    for file in files:
        print(str(cont) + ". " + file)
        cont += 1
    while respuesta == False:
        numArchivo = raw_input('\n')
        for file in files:
            if file == files[int(numArchivo) - 1]:
                respuesta = True
                break
    return files[int(numArchivo) - 1]


def sintac_getErrores():
    return errores

def sintac_getPrints():
    return prints

def sintac_getArduino():
    return arduino

# Funcion para limpiar los valores de la lista de errores
def limpiarErrores():
    errores.clear()
def limpiarNombres():
    nombres.clear()
def limpiarPrints():
    prints.clear()