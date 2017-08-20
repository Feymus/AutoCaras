import numpy as np
import cv2
from Model.Sujeto import Sujeto
import os  #libreria para contar la cantidad de fotos por carpeta del sujeto


# Pruebas con OpenCV, PIL y numpy
# Consigo la direccion donde se encuentra la imagen
scriptDir = os.path.dirname(__file__)
contador = 0 #contador que recorre imagen por imagen
dirs = [d for d in os.listdir('../Images/') if os.path.isdir(os.path.join('../Images/', d))]
lista = os.listdir('../Images/') # devuelve cantidad de fotos en direccion dada
print(dirs)
print(str(len(dirs)))

numeroImagenes = len(lista) #numero de imagenes en direccion
matrizImgVec = [[]]

while (contador+1<=2):
    impath = os.path.join(scriptDir,'../Images/s1/'+str(contador+1)+'.pgm') #esta direccion es proporcionada por el usuario
    
    # Primeras pruebas de vectorizacion
    arr = cv2.imread(impath,0) # Matriz de una imagen en escala de grises
    arr = cv2.resize(arr, (112, 92)) # Reescalamos la imagen para que sea 112*92
    flat_arr = arr.ravel() # Vectorizacion de una matriz

    if (contador+1 == 1):   #si contador es 1, agrega los elementos como vectores
        for m in flat_arr:
            matrizImgVec.append([m])
    else:   # sino solo los agrega a la columna respectiva
        y=1
        for p in flat_arr:
            matrizImgVec[y].append(p)
            y+=1  
    contador+=1
    
    
del matrizImgVec[0] #elimina el primer elemento que era vacio
print("where are you ? ")
print (matrizImgVec)
print("Cantidad de imagenes: " + str(len(matrizImgVec[0])))
print("Tamano: " + str(len(matrizImgVec)))    

'''
m = np.cov(matrizImgVec)
print(m)
print(len(m))
print(len(m[0]))
'''

if __name__ == "__main__":
    m = np.cov([[1,2],[3,4]])
    print(m)




    