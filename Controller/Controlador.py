##@package docstring
#Created on Aug 16, 2017
#
#@author: Michael Choque
#@author: Nelson G�mez
#@author: William Espinoza

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
    
    ## Metodo AgregarSujeto
    #
    # @param dict_sujeto un diccionario con el nombre del sujeto y una lista con sus imagenes
    # @return True/False segun si se agrega con exito el sujeto
    def AgregarSujeto(self, dict_sujeto):
        return self.listaDeSujetos.Agregar(dict_sujeto)
    
    ## Metodo CargarImagenes
    #
    # @param img_url la direccion local de donde se van a sacar los sujetos y sus imagenes
    # @return una tupla con informacion de si se realizo bien o mal
    # Ejm de una ruta valida:
    # direccion valida C:/Users/HP/Desktop/TEC/II Semestre 2017/Aseguramiento de calidad/Proyecto/AutoCaras/Images
    def CargarImagenes(self, img_url):

        try:
            # Se saca todos los nombres de carpetas en la ruta dada, estos pasan a ser los nombres de los sujetos
            sujetos = [sujeto for sujeto in os.listdir(img_url) 
                            if os.path.isdir(os.path.join(img_url, sujeto))]
            
            print(sujetos)

            for sujeto in sujetos:

                #Ahora por cada sujeto se sacan los nombres de las imagenes en su respectiva carpeta
                imgspath = os.listdir(img_url + '/' + sujeto)
                dict_sujeto = {}
                dict_sujeto["nombre"] = sujeto
                dict_sujeto["fotos"] = []
                
                for img in imgspath:
                    
                    # Por ruta de imagen, la abrimos y transformamos la imagen
                    if (img != "10.pgm"):
                        path = img_url + '/' + sujeto + '/' + img
                        arr = cv2.imread(path, 0) # Matriz de una imagen en escala de grises
                        arr = cv2.resize(arr, (112, 92)) # Reescalamos la imagen para que sea 112*92
                        dict_sujeto["fotos"].append(arr)
                        
                        # Se guarda el sujeto y sus imagenes en memoria
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
        matrizImgVec, mean = self.DefinirMatrizDeImagenes(imgs)
        matrizDeCov = self.DefinirMatrizDeCovarianza(matrizImgVec)
        auto_valores, auto_vectores = self.DefinirAutoValoresVectores(matrizDeCov, matrizImgVec)
        pesos = self.DefinirPesos(matrizImgVec, auto_vectores)
        print(pesos)
        id = self.Clasificar('C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images\\s41\\10.pgm', mean, auto_vectores, pesos)
        return self.listaDeSujetos.GetSujetoAt(id)

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
        
        numeroImagenes = len(listImgs) #numero de imagenes a recorrer
        print(numeroImagenes)
        matrizImgVec = np.empty(shape=(10304, numeroImagenes))#se crea la matriz que contendra las imagenes vectorizadas
        
        
        img_id = 0

        for training_img in listImgs:
            
            imgVectorizada = self.VectorizarImagen(training_img)
            matrizImgVec[:, img_id] = imgVectorizada[:]
            img_id += 1

        mean_img = np.sum(matrizImgVec, axis=1) / numeroImagenes

        for j in range(0, numeroImagenes):
            matrizImgVec[:, j] -= mean_img[:]
        
        return (matrizImgVec, mean_img)
    
    ## Metodo DefinirMatrizDeCovarianza
    #
    # @param matrizImgVec el metodo recibe una matriz de imagenes vectorizadas con la que se calculara la matriz de covarianza
    # @return matrizCov se devuelve la matriz de covarianza calculada 
    def DefinirMatrizDeCovarianza(self, matrizImgVec):
        matrizCov = np.matrix(matrizImgVec.transpose()) * np.matrix(matrizImgVec)                             
        matrizCov /= len(matrizImgVec[0])
        return matrizCov
    
    def DefinirAutoValoresVectores(self, matrizCov, matrizImgVec):
        
        auto_valores, auto_vectores = np.linalg.eig(matrizCov)
        indices = auto_valores.argsort()[::-1]
        auto_valores = auto_valores[indices]
        auto_vectores = auto_vectores[indices]

        suma_AV = sum(auto_valores[:])
        contador_AV = 0
        energia_AV = 0.0
        
        for auto_valor in auto_valores:
            contador_AV += 1
            energia_AV += auto_valor / suma_AV

            #if energia_AV >= 0.85:
            #    break

        auto_valores = auto_valores[0:contador_AV]
        auto_vectores = auto_vectores[0:contador_AV]

        auto_vectores = auto_vectores.transpose()
        auto_vectores = matrizImgVec * auto_vectores                            
        norms = np.linalg.norm(auto_vectores, axis=0)                           
        auto_vectores = auto_vectores / norms                                   

        return (auto_valores, auto_vectores)
    
    def DefinirPesos(self, matrizImgVec, auto_vectores):
        return auto_vectores.transpose() * matrizImgVec
        
    def Clasificar(self, img_dir, mean, auto_vectores, pesos):
        
        img = cv2.imread(img_dir, 0)
        img_col = np.array(img, dtype='float64').flatten()
        img_col[:] -= mean[:]
        img_col = np.reshape(img_col, (10304, 1))

        S = auto_vectores.transpose() * img_col

        diff = pesos - S
        norms = np.linalg.norm(diff, axis=0)

        id_cercano = np.argmin(norms)
        return (id_cercano // 9) + 1

    