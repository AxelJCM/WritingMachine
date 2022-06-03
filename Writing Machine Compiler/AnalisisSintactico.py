import ply.yacc as yacc
import os
import codecs
import re
from AnalisisLexico import *
from AnalisisSemantico import runSemanticAnalizer
from sys import stdin
from pip._vendor.distlib.compat import raw_input
import random

contproc = 0
global contmain
contmain = 0

precedence = (
    ('right', 'PUNTOCOMA'),
    #('left', 'DIFERENTE'),
    ('left', 'BRACKET2'),
    ('right', 'BRACKET1'),
    ('right', 'IGUAL_IGUAL', 'IGUAL', 'NEGACION'), 
    ('right', 'COMA'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'SMALLER', 'GREATER', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'DIVISION', #'DIV_ENTERA'
      'MULTI'),
    ('left', 'EXPONENTE'),
    ('left', 'CIERRA_P'),
    ('right', 'ABRE_P'), 
)


# Define las listas necesarias

nombres = {}

arduino = {}

prints = []

errores = []

data = []

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
            '''
    global contproc
    global contmain
    contmain = 0
    if p[1] == '\//.*':
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]
    
def p_procedimiento(p): # no puede haber otro procedimiento dentro de un procedimiento, funcion?
    
    '''
    procedimiento : PARA ID BRACKET1 condicion BRACKET2 cuerpo2 FIN cuerpo
                  | PARA ID BRACKET1 variable BRACKET2 cuerpo2 FIN cuerpo
                  | PARA ID BRACKET1 parametro BRACKET2 cuerpo2 FIN cuerpo
    '''
    
    global contproc
    if p[8] != '$':
        p[0] = (p[2], p[4], p[6],p[8])
        print(p[7] + "1")
    else:   
        p[0] = (p[2], p[4],p[6])
        print(p[7] + "2")
        
def p_llamadoproc(p):
    '''
    llamadoproc : PARA ID BRACKET1 parametro BRACKET2 PUNTOCOMA
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
    nombres[p[2]] = [p[4]]
    p[0] = (p[1], p[2], p[3], p[4])
    print(p[2], p[3], p[4])
    print(nombres)



def p_expresion(p):
    '''
    expresion : NUMERO expresion
              | funcion expresion
              | ID expresion
              | VAR expresion
              | expresion_alge1 expresion
              | expresion_alge2 expresion
              | Sum expresion
              | Substr expresion
              | Mult expresion
              | Div expresion
              | STRING expresion
              | NUMERO empty
              | COMA empty
              | ID empty
              | VAR empty
              | STRING empty
              | empty empty
                        
    '''

    if (p[2] != '$'):
        p[0] = (p[1], p[2])
    else:
        errores.append("Error de sintaxis, no se puede escribir un ID, coma, string, numero o variable solo")
        

def p_funcion(p):
    '''
    funcion : Random
            | Beginning
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

def p_Str(p):
    '''
    String : COMILLAS STRING COMILLAS
    '''
    p[0] = p[2]
    


def p_Put(p): # se puede mejorar con "expresion" Tambien puede sumarse una 
    # variable numerica o uno de tipo "funcion"
    '''
    Put : PUT VAR COMA NUMERO PUNTOCOMA
        | PUT VAR COMA expresion_alge1 PUNTOCOMA
        | PUT VAR COMA expresion_alge2 PUNTOCOMA 
    '''
    nombres[p[2]] = p[4]
    p[0] = (p[1], p[2], p[3], p[4])
    
def p_condicion(p):
    '''
    condicion : Equal
              | Greater
              | Smaller
              | GreaterEq
              | SmallerEq
    '''
    p[0] = p[1]    
    
def expresion_alge(p):
    '''
    expresion_alge : expresion_alge1
                   | expresion_alge2
                   
    '''
    

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
    elif p[2] == '**' : p[0] = p[1]**p[3]

    print(p[0])

def p_expresion_alge2(p):

    '''
    expresion_alge2 : ABRE_P expresion_alge1 CIERRA_P SUMA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P RESTA ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P MULT ABRE_P expresion_alge1 CIERRA_P
                   | ABRE_P expresion_alge1 CIERRA_P DIV ABRE_P expresion_alge1 CIERRA_P
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
        | SUM ABRE_P NUMERO COMA VAR CIERRA_P
        | SUM ABRE_P VAR COMA NUMERO CIERRA_P
        | SUM ABRE_P VAR COMA VAR CIERRA_P
    '''

    p[0] = int(p[3]) + int(p[5])
    print(p[0])


def p_Substr(p):
    '''
    Substr : SUBSTR ABRE_P NUMERO COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
           | SUBSTR ABRE_P NUMERO COMA VAR CIERRA_P
           | SUBSTR ABRE_P VAR COMA NUMERO CIERRA_P
           | SUBSTR ABRE_P VAR COMA VAR CIERRA_P
    '''

    p[0] = int(p[3]) - int(p[5])
    print(p[0])

def p_Mult(p):
    '''
    Mult : MULT ABRE_P NUMERO COMA NUMERO CIERRA_P
         | MULT ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
         | MULT ABRE_P NUMERO COMA VAR CIERRA_P
         | MULT ABRE_P VAR COMA NUMERO CIERRA_P
         | MULT ABRE_P VAR COMA VAR CIERRA_P
    '''

    p[0] = int(p[3]) * int(p[5])
    print(p[0])

def p_Div(p):
    '''
    Div : DIV ABRE_P NUMERO COMA NUMERO CIERRA_P
        | DIV ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
        | DIV ABRE_P NUMERO COMA VAR CIERRA_P
        | DIV ABRE_P VAR COMA NUMERO CIERRA_P
        | DIV ABRE_P VAR COMA VAR CIERRA_P
    '''

    p[0] = int(p[3]) / int(p[5])
    print(p[0])

###### CAMBIAR NOMBRES DE PALABRAS RESERTVADAS SI SE VA A USAR
#def p_Power(p):
   # '''
   # Power  : POWER ABRE_P NUMERO COMA NUMERO CIERRA_P
   #        | POWER ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P
   #        | POWER ABRE_P NUMERO COMA VAR CIERRA_P
   #        | POWER ABRE_P VAR COMA NUMERO CIERRA_P
   #        | POWER ABRE_P VAR COMA VAR CIERRA_P
 #   '''

   # p[0] = p[3] ** p[5]
   # print(p[0])



def p_Equal(p):
    '''
    Equal : EQUAL ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P NUMERO COMA ID CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P ID COMA NUMERO CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P expresion_alge1 COMA ID CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P ID COMA expresion_alge1 CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P expresion_alge2 COMA ID CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P ID COMA expresion_alge2 CIERRA_P PUNTOCOMA
            | EQUAL ABRE_P expresion_alge2 COMA expresion_alge2 CIERRA_P PUNTOCOMA
    '''

    if p[3] == p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])

def p_Greater(p):
    '''
    Greater : GREATER ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
            | GREATER ABRE_P NUMERO COMA ID CIERRA_P PUNTOCOMA
            | GREATER ABRE_P ID COMA NUMERO CIERRA_P PUNTOCOMA
            | GREATER ABRE_P expresion_alge1 COMA ID CIERRA_P PUNTOCOMA
            | GREATER ABRE_P ID COMA expresion_alge1 CIERRA_P PUNTOCOMA
            | GREATER ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
            | GREATER ABRE_P expresion_alge2 COMA ID CIERRA_P PUNTOCOMA
            | GREATER ABRE_P ID COMA expresion_alge2 CIERRA_P PUNTOCOMA
            | GREATER ABRE_P expresion_alge2 COMA expresion_alge2 CIERRA_P PUNTOCOMA
            
    '''
    
    if p[3] > p[5]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])


def p_Smaller(p):
    '''
    Smaller : SMALLER ABRE_P NUMERO COMA NUMERO CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P NUMERO COMA ID CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P ID COMA NUMERO CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P expresion_alge1 COMA ID CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P ID COMA expresion_alge1 CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P expresion_alge1 COMA expresion_alge1 CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P expresion_alge2 COMA ID CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P ID COMA expresion_alge2 CIERRA_P PUNTOCOMA
            | SMALLER ABRE_P expresion_alge2 COMA expresion_alge2 CIERRA_P PUNTOCOMA
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



#def p_Diferente(p):
#    '''
 #   Diferente : NUMERO DIFERENTE NUMERO
#          | VAR DIFERENTE VAR
#          | NUMERO DIFERENTE VAR
 #         | VAR DIFERENTE NUMERO
#    '''

#    if p[1] != p[3]:
 #       p[0] = True
 #   else:
 #       p[0] = False
#
 #   print(p[0])


def p_GreaterEq (p):
    '''
    GreaterEq : NUMERO MAYORIGUAL NUMERO
            | VAR MAYORIGUAL VAR
            | NUMERO MAYORIGUAL VAR
            | VAR MAYORIGUAL NUMERO
    '''

    if p[1] >= p[3]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])

def p_SmallerEq (p):
    '''
    SmallerEq : NUMERO MENORIGUAL NUMERO
            | VAR MENORIGUAL VAR
            | NUMERO MENORIGUAL VAR
            | VAR MENORIGUAL NUMERO
    '''

    if p[1] <= p[3]:
        p[0] = True
    else:
        p[0] = False

    print(p[0])


def p_If(p): # en lugar de condicion tambien puede tener exp_alg1 y 2
    # funcion debe ir separado por ; (lo mismo que Run)

    '''
    If : IF ABRE_P condicion CIERRA_P BRACKET1 funcion BRACKET2 ENDIF
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

def p_While(p):
    # condicion puede ser tambien exp_alg1y2
    # funciones separadas por ;
    ''' 
    While : WHILE BRACKET1 condicion BRACKET2 BRACKET1 funcion BRACKET2 
    
    '''
    print(p[3])

    while(p[3]):
        p[0] = p[6]

def p_Repeat(p): ################## REVISAR QUE FUNCIONE BIEN ##############################################
    #### Lo de funcion igual que Run
    ''' 
    Repeat : REPEAT NUMERO BRACKET1 funcion BRACKET2
    
    '''

    #p[0] = p[4]*p[2]
    for i in range(p[2]):
         p[0] = p[4]

def p_until(p): ################ revisar funcionamiento
    ### funcion y condicion como IfElse
    ''' 
    Until : UNTIL BRACKET1 funcion BRACKET2 BRACKET1 condicion BRACKET2
    '''
    p[0] = p[3]
    while True:
        p[0] = p[3]
        if(p[6]):
            break
        
    

def p_add(p): # tambien sumar con exp_alg1y2

    '''
    Add : ADD ABRE_P VAR empty empty CIERRA_P PUNTOCOMA
        | ADD ABRE_P VAR COMA NUMERO CIERRA_P PUNTOCOMA
        | ADD ABRE_P VAR COMA VAR CIERRA_P PUNTOCOMA
    
    '''
    if p[4] == '$':
        p[0]= p[3]+1
    else:
        p[0]= p[3]+ p[5]
    

def p_parametro(p): 
    '''
    parametro : VAR COMA parametro
              | VAR empty empty
              | NUMERO COMA parametro
              | NUMERO empty empty
              | empty empty empty
    '''
    if p[3] != '$' and p[2] != '$':
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_beginning(p):
    '''
    Beginning : BEGINNING PUNTOCOMA
    '''
    p[0] = p[1]
    print("Beginning")
    #data.append("Begin:")
    #data.append(str(0))
    #writeToJSONFile(path,fileName,data)

def p_random(p):
    '''
    Random : RANDOM ABRE_P NUMERO CIERRA_P PUNTOCOMA'''
    
    p[0] = random.randrange(p[3])
    print(p[0])


def p_ContinueUp(p): # recibe numero, operacion aritmetica, variables
    '''
    ContinueUp : CONTINUEUP NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueUp " + str(p[2]))
    data['ContinueUp'] = str(p[2])
    data.append("ContinueUp:"+ str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_ContinueDown(p): # recibe numero, operacion aritmetica, variables
    '''
    ContinueDown : CONTINUEDOWN NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueDown " + str(p[2]))
    #data['ContinueDown'] = str(p[2])
    #data.append("ContinueDown:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_ContinueRight(p): # recibe numero, operacion aritmetica, variables
    '''
    ContinueRight : CONTINUERIGHT NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print("ContinueRight " + str(p[2]))
    #data['ContinueRight'] = str(p[2])
    #data.append("ContinueRight:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_ContinueLeft(p): # recibe numero, operacion aritmetica, variables
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
    #data.append("Up:")
    #data.append(str(0))
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

def p_Pos(p): # recibe numero, operacion aritmetica, variables
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

def p_PosX(p): # recibe numero, operacion aritmetica, variables
    
    '''
    PosX : POSX NUMERO PUNTOCOMA
         | POSX expresion PUNTOCOMA
    '''

    p[0] = p[2]
    print ("Coordenada X = "+ str(p[2]))
    #data['PosX'] = str(p[2])
    #data.append("PosicionX:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)
 

def p_PosY(p): # recibe numero, operacion aritmetica, variables
    
    '''
    PosY : POSY NUMERO PUNTOCOMA
    '''

    p[0] = p[2]
    print ("Coordenada Y = "+ str(p[2]))
    #data['PosY'] = str(p[2])
    #data.append("PosicionY:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)

def p_UseColor(p): # talvez tambien usar variables 
    
    '''
    UseColor : USECOLOR NUMERO PUNTOCOMA
            | USECOLOR empty PUNTOCOMA
    '''
    
    if p[2] in range(1,2):
        p[0] = p[2]
        print("UseColor "+ str(p[2]))
    elif p[2] == '$':
        p[0] = 1
    else:
        print("Error")
        # llamar a la funcion de error por index out of bounds

    #data['Color'] = str(p[2])
    #data.append("Color:")
    #data.append(str(p[2]))
    #writeToJSONFile(path,fileName,data)


def p_Run(p): # corresponde al cuerpo de las instrucciones. Usar ; al final
        # funcion debe tener funciones separadas por ;
        # para esto se puede hacer mas | RUN ...
    '''
    Run : RUN BRACKET1 funcion BRACKET2 
    '''

    p[0] = p[3]
    print ("Running " + str(p[3]))

def p_PrintLine(p): # hacer lo del string para que se reconozca
    # Hacer lista para cada uno de estos prints y asi poder llevarlos al ide como los errores
    # lo de expresion puede ser solo una cadena, solo una variable, solo un numero, o una combinacion de todas separados por coma

    ''' PrintLine : PRINTLINE ABRE_P expresion CIERRA_P PUNTOCOMA'''
    print(p[3])
    if p[3] == ',':
        print("si hay coma")
        p[0] = p[3]
    else:
        p[0] = p[3]
        prints.append(p[3])
        print(prints)
 

def p_empty(p):
    '''
    empty :
    '''
    p[0] = '$'


def p_error(p):
    print("se encuentra error")
    if p is not None:
        errores.append("Error de sintaxis ({}) en linea {}".format(str(p.value), str(p.lineno)))
        print(errores)
    else:
        print(str(p.value))
        errores.append("Error de sintaxis")
        
    
    
parser = yacc.yacc()

def sintacticAnalizer(cadena):
    parser = yacc.yacc()
    parser.parse(cadena)

#cad = "// dadaw \n Para Axel[mario]\n Para Chris[dawdaw]\n Fin\n Fin"
#sintacticAnalizer(cad)
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


def sintac_getErrores():
    return errores

def sintac_getPrints():
    return prints