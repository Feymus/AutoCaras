import numpy as np
import os
import cv2
from Controller.GestorGeneral import GestorGeneral
from Controller.GestorSujeto import GestorSujeto
from Model.Sujeto import Sujeto
import os  #libreria para contar la cantidad de fotos por carpeta del sujeto


# Pruebas con OpenCV, PIL y numpy
# Consigo la direccion donde se encuentra la imagen
scriptDir = os.path.dirname(__file__)
contador = 0 #contador que recorre imagen por imagen
list = os.listdir('C:/Users/Nelson/AutoCaras/Images/s1') # devuelve cantidad de fotos en direccion dada
numeroImagenes = len(list) #numero de imagenes en direccion
matrizImgVec = [[]]

while (contador+1<=numeroImagenes):
    impath = os.path.join(scriptDir,'../Images/s1/'+str(contador+1)+'.pgm') #esta direccion es proporcionada por el usuario
    
    # Primeras pruebas de vectorizacion
    arr = cv2.imread(impath,0) # Matriz de una imagen en escala de grises
    flat_arr = arr.ravel() # Vectorizacion de una matriz
     
    if (contador+1 ==1):   #si contador es 1, agrega los elementos como vectores
        for m in flat_arr:
            matrizImgVec.append([m])
    else:   # sino solo los agrega a la columna respectiva
        y=1
        for p in flat_arr:
            matrizImgVec[y].append(p)
            y+=1  
    contador+=1
    
    
del matrizImgVec[0] #elimina el primer elemento que era vacio
print (matrizImgVec)    
print("muy bien")
#[131 129 127 ...,  27  27  25]
#[134 135 136 ...,  29  29  18]
#[142 143 143 ...,  36  30  26]
#[145 144 145 ...,  35  30  31]
#[140 140 143 ...,  40  37  31]
#[146 145 148 ...,  35  33  30]
#[141 140 134 ...,  21  18  18]
#[129 129 129 ...,  17  14  18]
#[142 144 144 ...,  25  30  29]
#[121 148 142 ...,  34  29  24]










    