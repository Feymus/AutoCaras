##@package docstring
#Created on Aug 16, 2017
#
#@author: Michael Choque

from Controller.GestorSujeto import GestorSujeto
import numpy as np
import os, sys, cv2

## Clase controlador
#
# Esta clase es la que permite la comunicacion entre los datos de la aplicacion y la interfaz de usuario
class Controlador(object):

    ## Constructor de la clase
    # 
    # El constructor unicamente inicializa la lista de Sujetos en la aplicacion
    def __init__(self):
        self.listaDeSujetos = GestorSujeto()
        
    
    def AgregarSujeto(self, dict_sujeto):
        return self.listaDeSujetos.Agregar(dict_sujeto)
    
    # direccion valida C:/Users/HP/Desktop/TEC/II Semestre 2017/Aseguramiento de calidad/Proyecto/AutoCaras/Images
    def CargarImagenes(self, img_url):

        try:
            sujetos = [sujeto for sujeto in os.listdir(img_url) 
                            if os.path.isdir(os.path.join(img_url, sujeto))]
    
            for sujeto in sujetos:
                imgspath = os.listdir(img_url + '/' + sujeto)
                dict_sujeto = {}
                dict_sujeto["nombre"] = sujeto
                dict_sujeto["fotos"] = []
                
                for img in imgspath:
                    path = img_url + '/' + sujeto + '/' + img
                    arr = cv2.imread(path, 0) # Matriz de una imagen en escala de grises
                    arr = cv2.resize(arr, (112, 92)) # Reescalamos la imagen para que sea 112*92
                    dict_sujeto["fotos"].append(arr)
                    self.AgregarSujeto(dict_sujeto)
                    
            return (0, "Carga completada!") 
        
        except FileNotFoundError as FNF:
            print(FNF)
            return (-1, "Error: Direccion no encontrada")
        except:
            print("Error inesperado: ", sys.exc_info()[0])
            return (-1, "Error: Desconocido")
        
    def Entrenar(self):
        imgs = self.listaDeSujetos.getAllImgs()
        matrizImgVec = self.DefinirMatrizDeImagenes(imgs)
        matrizDeCov = self.DefinirMatrizDeCovarianza(matrizImgVec)
        return matrizDeCov
    
    ##Funcion que vectoriza una imagen que le entra por parametro
    #@param img recibe la imagen
    #@return flat_img devuelve la lista de una imagen vectorizada.
    def VectorizarImagen(self, img):
        flat_img = img.ravel() # Vectorizacion de una matriz
        return flat_img   
    
    ##Funcion que crea la matriz con las imagenes vectorizadas
    #@param listImgs la lista de la imagen ya vectorizada
    #@return MatrizImgVec es la matriz con todas las imagenes vectorizadas de un sujeto
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
    