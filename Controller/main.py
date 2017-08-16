'''
Created on Aug 12, 2017

@author: Michael
'''

import numpy as np
from PIL import Image
import os
import cv2
from Controller.GestorGeneral import GestorGeneral
from Controller.GestorSujeto import GestorSujeto
from Model.Sujeto import Sujeto


# Pruebas con OpenCV, PIL y numpy
# Consigo la direccion donde se encuentra la imagen
scriptDir = os.path.dirname(__file__)
impath = os.path.join(scriptDir, '../Images/unnamed.jpg')


# Matriz de una imagen (la imagen misma)
image = cv2.imread(impath)
# Cambio a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#Cambio de tamano de la imagen
#gray_image = cv2.resize(gray_image, (100, 100))

 
cv2.imshow("Over the Clouds", image)
cv2.imshow("Over the Clouds - gray", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Primeras pruebas de vectorizacion
#arr = cv2.imread(impath,0) # Matriz de una imagen en escala de grises
#flat_arr = arr.ravel() # Vectorizacion de una matriz
#print(flat_arr)
#[240 240 240 ..., 229 229 229]


# Vectorizacion segun el documento que paso William
#arr = np.asarray(gray_image, dtype = np.uint8)
#print(arr)
#[[240 240 240 ..., 235 235 235]
#[240 240 240 ..., 235 235 235]
#[240 240 240 ..., 235 235 235]
#..., 
#[230 230 230 ..., 229 229 229]
#[230 230 230 ..., 229 229 229]
#[230 230 230 ..., 229 229 229]]


# Pruebas con PIL
#img = Image.open(impath).convert('RGB')
#arr = np.array(img)
#flat_arr = arr.ravel()
#print(flat_arr)

if __name__ == '__main__':
    pass
    