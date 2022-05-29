import ply.yacc as yacc
import os
import codecs
import re
from AnalisisLexico import tokens
from AnalisisLexico import GenerarTok
from AnalisisSemantico import runSemanticAnalizer
from sys import stdin
from pip._vendor.distlib.compat import raw_input
import random

precedence = (
    ('right', 'PUNTOCOMA'),
    #('left', 'DIFERENTE'),
    ('left', 'BRACKET2'),
    ('right', 'BRACKET1'),
    ('right', 'IGUAL_IGUAL', 'IGUAL', 'NEGACION'), 
    ('right', 'COMA'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'SMALLERTHEN', 'GREATERTHEN', 'GREATER', 'SMALLER'),
    ('left', 'DIVISION', 'DIV_ENTERA', 'MULTI'),
    ('left', 'EXPONENTE'),
    ('left', 'CIERRA_P'),
    ('right', 'ABRE_P'), 
)


# Define las listas necesarias

nombres = {}

errores = []

data = []

# Funciones para el arbol

def p_Start(p):
    '''
    Start : code
    '''
    #runSemanticAnalizer(p[1])
        
def p_Code(p):
    '''
    code : PARA VAR BRACKET1 VAR BRACKET2 cuerpo
    '''
    p[0] =  p[6]
    


def p_cuerpo(p):
    '''
    cuerpo : variable
           | expresion
           '''
    p[0] = p[1]


def p_Variable(p):
    '''
    variable : variable1 cuerpo
            | variable2 cuerpo
            | variable3 cuerpo
            | variable4 cuerpo
            | empty empty
    '''
    if (p[2] != '$'):
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


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
    nombres[p[2]] = p[4]
    p[0] = (p[1], p[2], p[3], p[4])
    print(p[2], p[3], p[4])
    print(nombres)


def p_Variable3(p):
    '''
    variable3 : PUT VAR IGUAL NUMERO PUNTOCOMA
              
    '''
    nombres[p[2]] = p[4]
    p[0] = (p[1], p[2], p[3], p[4])
    print(p[2], p[3], p[4])
    print(nombres)

def p_Variable4(p):
    '''
    variable4 : PUT VAR IGUAL expresion_alge1 PUNTOCOMA
              | PUT VAR IGUAL expresion_alge2 PUNTOCOMA
              
    '''
    nombres[p[2]] = p[4]
    p[0] = (p[1], p[2], p[3], p[4])
    print(p[2], p[3], p[4])
    print(nombres)
    



def p_expresion(p):
    '''
    expresion : NUMERO expresion
              | funcion expresion
              | VAR expresion
              | condicion expresion
              | expresion_alge1 expresion
              | expresion_alge2 expresion
              | Sum expresion
              | Substr expresion
              | Mult expresion
              | Div expresion
              | empty empty
                        
    '''

    if (p[2] != '$'):
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]
        

def p_funcion(p):
    '''
    funcion : Random
            | Begining
            | ContinueUp
            | ContinueDown
            | ContinueRight
            | ContinueLeft
            | Up
            | Down
            | Speed
            | Pos
            | PosX
            | PosY
            | UseColor
            | Run
            | If
            | IfElse
            | Repeat
            | Until
            | While
            | PrintLine
            | And
            | Or
            | Add
            | Put
         
       
    '''
    p[0] = p[1]


def p_condicion(p):
    '''
    condicion : Equal expresion
              | Greater expresion
              | Mayor expresion
              | Smaller expresion
              | Greaterthen expresion
              | Smallerthen expresion 
    '''
    
def expresion_alge(p):
    '''
    expresion_alge : expresion_alge1
                   | expresion_alge2
                   
    '''
    

def p_expresion_alge1(p):

    '''
    expresion_alge1 : NUMERO SUMA NUMERO 
                   | NUMERO RESTA NUMERO 
                   | NUMERO MULTIPLICA NUMERO 
                   | NUMERO DIVIDE NUMERO
                   | NUMERO EXPONENTE NUMERO
                   
    '''

    if p[2] == '+' : p[0] = p[1]+p[3]
    elif p[2] == '-' : p[0] = p[1]-p[3]
    elif p[2] == '*' : p[0] = p[1]*p[3]
    elif p[2] == '/' : p[0] = p[1]/p[3]
    elif p[2] == '**' : p[0] = p[1]**p[3]

    print(p[0])

def p_expresion_alge2(p):

    '''
    expresion_alge2 : ABRE_P expresion_alge1 CIERRA_P SUMA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P RESTA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P MULTIPLICA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P DIVIDE ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P POTENCIA ABRE_P expresion_alge1 CIERRA_P
                   
    '''

    if p[4] == '+' : p[0] = p[2]+p[6]
    elif p[4] == '-' : p[0] = p[2]-p[6]
    elif p[4] == '*' : p[0] = p[2]*p[6]
    elif p[4] == '/' : p[0] = p[2]/p[6]
    elif p[4] == '^' : p[0] = p[2]**p[6]
    

def p_Sum(p):
    '''
    Sum : SUM ABRE_P NUMERO COMA NUMERO CIERRA_P
        | SUM ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
        | SUM ABRE_P NUMERO COMA ID CIERRA_P
    '''

    p[0] = p[3] + int(p[5])
    print(p[0])


def p_Substr(p):
    '''
    Substr : SUBSTR ABRE_P NUMERO COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
           | SUBSTR ABRE_P NUMERO COMA ID CIERRA_P
           | SUBSTR ABRE_P ID COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P ID COMA ID CIERRA_P
    '''

    p[0] = p[3] - p[5]
    print(p[0])

def p_Mult(p):
    '''
    Mult : MULT ABRE_P NUMERO COMA NUMERO CIERRA_P
         | MULT ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
         | MULT ABRE_P NUMERO COMA ID CIERRA_P
         | MULT ABRE_P ID COMA NUMERO CIERRA_P
         | MULT ABRE_P ID COMA ID CIERRA_P
    '''

    p[0] = p[3] * p[5]
    print(p[0])

def p_Div(p):
    '''
    Div : DIV ABRE_P NUMERO COMA NUMERO CIERRA_P
        | DIV ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
        | DIV ABRE_P NUMERO COMA ID CIERRA_P
        | DIV ABRE_P ID COMA NUMERO CIERRA_P
        | DIV ABRE_P ID COMA ID CIERRA_P
    '''

    p[0] = p[3] / p[5]
    print(p[0])

#def p_Power(p):
   # '''
   # Power  : POWER ABRE_P NUMERO COMA NUMERO CIERRA_P
   #        | POWER ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
   #        | POWER ABRE_P NUMERO COMA ID CIERRA_P
   #        | POWER ABRE_P ID COMA NUMERO CIERRA_P
   #        | POWER ABRE_P ID COMA ID CIERRA_P
 #   '''

   # p[0] = p[3] ** p[5]
   # print(p[0])



def p_Equal(p):
    '''
    Equal : EQUAL ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
    '''

    if p[3] == p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])

def p_Greater(p):
    '''
    Greater : GREATER ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
    '''
    
    if p[3] > p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])


def p_Smaller(p):
    '''
    Smaller : SMALLER ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
    '''
    
    if p[3] < p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])



def p_And(p):
    ''' And : AND ABRE_P expresion COMA expresion CIERRA_P PUNTOCOMA '''
    
    if p[3] == True and p[5] == True:
        p[0] = True
    else:
        p[0] = False




def p_Or(p):
    ''' Or : OR ABRE_P expresion COMA expresion CIERRA_P PUNTOCOMA '''

    p[0] = p[2] or p[5]




def p_Equal(p):
    '''
    Equal : NUMERO IGUAL NUMERO
          | ID IGUAL ID
          | NUMERO IGUAL ID
          | ID IGUAL NUMERO
    '''
    if p[1] == p[3]:
        p[0] = True
    else:
        p[0] = False


#def p_Diferente(p):
#    '''
 #   Diferente : NUMERO DIFERENTE NUMERO
#          | ID DIFERENTE ID
#          | NUMERO DIFERENTE ID
 #         | ID DIFERENTE NUMERO
#    '''

#    if p[1] != p[3]:
 #       p[0] = True
 #   else:
 #       p[0] = False
#
 #   print(p[0])


def p_Greater(p):
    '''
    Greater : NUMERO MAYOR NUMERO
          | ID MAYOR ID
          | NUMERO MAYOR ID
          | ID MAYOR NUMERO
    '''

    if p[1] > p[3]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])

def p_Smaller(p):
    '''
    Smaller : NUMERO MENOR NUMERO
          | ID MENOR ID
          | NUMERO MENOR ID
          | ID MENOR NUMERO
    '''

    if p[1] < p[3]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])

def p_Greaterthen (p):
    '''
    Greaterthen : NUMERO MAYORIGUAL NUMERO
          | ID MAYORIGUAL ID
          | NUMERO MAYORIGUAL ID
          | ID MAYORIGUAL NUMERO
    '''

    if p[1] >= p[3]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])

def p_Smallerthen (p):
    '''
    Smallerthen : NUMERO MENORIGUAL NUMERO
          | ID MENORIGUAL ID
          | NUMERO MENORIGUAL ID
          | ID MENORIGUAL NUMERO
    '''

    if p[1] <= p[3]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])


def p_If(p):

    '''
    If : IF condicion BRACKET1 funcion BRACKET2 ENDIF
    '''

    print(p[3])

    if(p[3]):
        p[0] = p[6]

def p_IfElse(p):

    '''
    IfElse : IFELSE condicion BRACKET1 funcion BRACKET2 BRACKET1 funcion BRACKET2
    '''

    if p[2]:
        p[0] = p[4]
    else:
        p[0] = p[7]

def p_While(p):

    ''' 
    While : WHILE BRACKET1 condicion BRACKET2 BRACKET1 funcion BRACKET2 
    
    '''
    print(p[3])

    while(p[3]):
        p[0] = p[6]

def p_Repeat(p):

    ''' 
    Repeat : REPEAT NUMERO funcion
    
    '''

    p[0] = p[3]*p[2]

def p_until(p):

    ''' 
    Until : UNTIL BRACKET1 funcion BRACKET2 BRACKET1 condicion BRACKET2
    '''

def p_add(p):

    '''
    Add : ADD ABRE_P VAR empty empty CIERRA_P
        | ADD ABRE_P VAR COMA NUMERO CIERRA_P
        | ADD ABRE_P VAR COMA VAR CIERRA_P
    
    '''

    p[0]= p[3]+ p[5]
    

def p_procedimiento(p):
    
    '''
    procedimiento : PARA ID BRACKET1 condicion BRACKET2 funcion FIN
                  | empty empty empty empty empty empty empty empty empty empty empty
    '''
    if p[11] != '$':
        p[0] = (p[1], p[2], p[4], p[6], p[8], p[9], p[10])
    elif p[11] == '$' and p[1] != '$':
        p[0] = (p[1], p[2], p[4], p[6], p[8], p[9])
    else:
        p[0] = p[1]


def p_parametro(p):
    '''
    parametro : ID COMA parametro
              | ID empty empty
              | NUMERO COMA parametro
              | NUMERO empty empty
              | empty empty empty
    '''
    if p[3] != '$' and p[2] != '$':
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_begining(p):
    '''
    Begining : BEGINING PUNTOCOMA
    '''
    p[0] = p[1]
    print("Begining")
    #data.append("Begin:")
    #data.append(str(0))
    #writeToJSONFile(path,fileName,data)

def p_random(p):
    '''
    Random : RANDOM ABRE_P NUMERO CIERRA_P PUNTOCOMA'''
    
    p[0] = random.randrange(p[3])
    print(p[0])


def p_ContinueUp(p):
    '''
    ContinueUp : CONTINUEUP NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueUp " + str(p[2]))
    #data['ContinueUp'] = str(p[2])
    #data.append("ContinueUp:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_ContinueDown(p):
    '''
    ContinueDown : CONTINUEDOWN NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueDown " + str(p[2]))
    #data['ContinueDown'] = str(p[2])
    #data.append("ContinueDown:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_ContinueRight(p):
    '''
    ContinueRight : CONTINUERIGHT NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueRight " + str(p[2]))
    #data['ContinueRight'] = str(p[2])
    #data.append("ContinueRight:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_ContinueLeft(p):
    '''
    ContinueLeft : CONTINUELEFT NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueLeft " + str(p[2]))
    #data['ContinueLeft'] = str(p[2])
    #data.append("ContinueLeft:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)


def p_Up(p):
    '''
    Up : UP PUNTOCOMA
    '''
    data.append("Up:")
    data.append(str(0))
    p[0] = p[1]
    print(p[0])
    #data['Lapiz'] = 'Up'
    
    #writeToJSONFile(path,fileName,data)

def p_Down(p):
    '''
    Down : DOWN PUNTOCOMA
    '''

    p[0] = p[1]
    print(p[0])
    #data['Lapiz'] = 'Down'
    #data.append("Down:")
    #data.append(str(0))
    #writeToJSONFile(path,fileName,data)

def p_Speed(p):
    '''
    Speed : SPEED NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("Velocidad = " + str(p[2]))
    #data['Speed'] = str(p[2])
    #data.append("Speed:")
    #data.append(str(p[2]))

    #writeToJSONFile(path,fileName,data)

def p_Pos(p):
    '''
    Pos : POS ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
    '''

    p[0] = (p[3],p[5])
    print ("Coordenada X = "+ str(p[3]))
    print("Coordenada Y = "+ str(p[5]))
    #data['Pos'] = str(p[3]) + "," + str(p[5])
    #data.append("PosicionX:")
    #data.append(str(p[3]))
    #data.append("PosicionY:")
    #data.append(str(p[5]))


    #writeToJSONFile(path,fileName,data)

def p_PosX(p):
    
    '''
    PosX : POSX NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print ("Coordenada X = "+ str(p[2]))
    #data['PosX'] = str(p[2])
    #data.append("PosicionX:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)
 

def p_PosY(p):
    
    '''
    PosY : POSY NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print ("Coordenada Y = "+ str(p[2]))
    #data['PosY'] = str(p[2])
    #data.append("PosicionY:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_UseColor(p):
    
    '''
    UseColor : USECOLOR NUMERO PUNTOCOMA
    '''

    if p[2] in range(1,4):
        print("UseColor "+ str(p[2]))
    else:
        print("Error")

    #data['Color'] = str(p[2])
    #data.append("Color:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)


def p_Run(p):

    '''
    Run : RUN BRACKET1 funcion BRACKET2
    '''

    p[0] = p[3]
    print ("Running " + str(p[3]))

def p_Print(p):

    ''' Print : PRINTLINE ABRE_P expresion CIERRA_P PUNTOCOMA'''
    p[0] = p[3]
    print(nombres[1].value)
 

def p_empty(p):
    '''
    empty :
    '''
    p[0] = '$'


def p_error(p):
    errores.append("Error de sintáxis en linea "+str(p.lineno))
    #errores.pop[len(errores)]
    print("error de sintaxis " + str(p))
    print("error en la linea " + str(p.lineno))


def sintacticAnalizer(cadena):
    parser = yacc.yacc()
    parser.parse(cadena)

cad = "//Hola soy sebas\nDef axel = 12;"
sintacticAnalizer(cad)
#def writeToJSONFile(path, fileName, data):
 #   filePathNameWExt = './' + path + '/' + fileName + '.json'
   # with open(filePathNameWExt, 'w') as fp:
   #     json.dump(data,fp)ContinueRight

#path = './'
#fileName = 'datosJSON'

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


