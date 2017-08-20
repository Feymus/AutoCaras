##@package docstring
#Created on Aug 16, 2017
#
#@author: Michael Choque

from Controller.GestorSujeto import GestorSujeto
import cv2
import numpy as np

## Clase controlador
#
# Esta clase es la que permite la comunicacion entre los datos de la aplicacion y la interfaz de usuario
class Controlador(object):

    ## Constructor de la clase
    # 
    # El constructor unicamente inicializa la lista de Sujetos en la aplicacion
    def __init__(self):
        self.listaDeSujetos = GestorSujeto()
    
    ##Funcion que vectoriza una imagen que le entra por parametro
    #@param recive la imagen
    #@return flat_arr, devuelve la lista de una imagen vectorizada.
    def VectorizarImagen(self, img):
        
        arr = cv2.imread(img,0) # Matriz de una imagen en escala de grises
        arr = cv2.resize(arr, (112, 92)) # Reescalamos la imagen para que sea 112*92
        flat_arr = arr.ravel() # Vectorizacion de una matriz
        
        return flat_arr   
    
    ##Funcion que crea la matriz con las imagenes vectorizadas
    #@param la lista de la imagen ya vectorizada
    #@return MatrizImgVec, es la matriz con todas las imagenes vectorizadas de un sujeto
    def DefinirMatrizDeImagenes(self, listImgs):
        
        contador = 0  #contador que lleva control de cuantas veces se ejecuta el ciclo while
        numeroImagenes = len(listImgs) #numero de imagenes a recorrer
        matrizImgVec = [[]]  #se crea la matriz que contendra las imagenes vectorizadas
        
        while (contador+1<=numeroImagenes):
            
            imgVectorizada = self.VectorizarImagen(listImgs[contador])  #llama a la funcion que vectoriza la imagen 
        
            if (contador+1 == 1):   #si es la primera imagen, agrega los elementos en un vector a la lista final
                for m in imgVectorizada:
                    matrizImgVec.append([m]) #va agregando a la lista final cada elemento de la lista 
            else:   # si no es la primer imagen, entonces va agregando a cada columna
                y=1
                for p in imgVectorizada:
                    matrizImgVec[y].append(p)  #agrega a la columna respectiva 
                    y+=1  
            contador+=1
        
        del matrizImgVec[0]
        
        return matrizImgVec
    
    ## Metodo DefinirMatrizDeCovarianza
    #
    # @param matrizImgVec el metodo recibe una matriz de imagenes vectorizadas con la que se calculara la matriz de covarianza
    # @return matrizCov se devuelve la matriz de covarianza calculada 
    def DefinirMatrizDeCovarianza(self, matrizImgVec):
        matrizCov = np.cov(matrizImgVec)
        return matrizCov
    