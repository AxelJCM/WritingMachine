import winsound

from pydub import *

s1 = "./prueba/iniciando_impresion.mp3"

sound = AudioSegment.from_mp3("C:/Users/sebas/OneDrive/Documentos/GitHub/WritingMachine/prueba/iniciando_impresion.mp3")
sound.export("C:/Users/sebas/OneDrive/Documentos/GitHub/WritingMachine/prueba/iniciando_impresion.wav", format="wav")

