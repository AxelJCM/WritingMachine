import ply.yacc as yacc
import os
import codecs
import re
from AnalisisLexico import tokens
from sys import stdin

precedence = (
    ('right', 'PUNTO_COMA'),
    ('left', 'DIFERENTE'),
    ('left', 'BRACKET2'),
    ('right', 'BRACKET1'),
    ('right', 'IGUAL_IGUAL', 'IGUAL', 'NEGACION'), 
    ('right', 'COMA'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'MAYOR_QUE', 'MENOR_QUE'),
    ('left', 'DIVISION', 'DIV_ENTERA', 'MULTI'),
    ('left', 'EXPONENTE'),
    ('left', 'CIERRA_P'),
    ('right', 'ABRE_P'),
)



