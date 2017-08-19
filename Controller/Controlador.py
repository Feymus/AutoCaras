'''
Created on Aug 16, 2017

@author: HP
'''
from Controller.GestorSujeto import GestorSujeto
import cv2
import numpy as np

class Controlador(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.listaDeSujetos = GestorSujeto()
    
    def VectorizarImagen(self, img):
        
        arr = cv2.imread(img,0) # Matriz de una imagen en escala de grises
        arr = cv2.resize(arr, (112, 92)) # Reescalamos la imagen para que sea 112*92
        flat_arr = arr.ravel() # Vectorizacion de una matriz
        
        return flat_arr
    
    def DefinirMatrizDeImagenes(self, listImgs):
        
        contador = 0
        numeroImagenes = len(listImgs)
        matrizImgVec = [[]]
        
        while (contador+1<=numeroImagenes):
            
            imgVectorizada = self.VectorizarImagen(listImgs[contador])
        
            if (contador+1 == 1):   #si contador es 1, agrega los elementos como vectores
                for m in imgVectorizada:
                    matrizImgVec.append([m])
            else:   # sino solo los agrega a la columna respectiva
                y=1
                for p in imgVectorizada:
                    matrizImgVec[y].append(p)
                    y+=1  
            contador+=1
        
        del matrizImgVec[0]
        
        return matrizImgVec
    
    def DefinirMatrizDeCovarianza(self, matrizImgVec):
        matrizCov = np.cov(matrizImgVec)
        return matrizCov
    