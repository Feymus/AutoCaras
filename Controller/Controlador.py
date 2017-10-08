"""Esta clase gestiona la interaccion entre la pagina web y el modelo
Gestiona el proceso de entrenamiento y clasificacion de sujetos"""
#Created on Aug 16, 2017
#
#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza
from __future__ import print_function
import os
import cv2
from Controller.GestorSujeto import GestorSujeto
import numpy as np


class Controlador(object):
    # pylint: disable=too-many-instance-attributes
    #se considera que los 8 atributos son necesarios
    """## Clase controlador
    #
    # Esta clase es la que permite la comunicacion entre los datos de la aplicacion
    y la interfaz de usuario"""
    ## Constructor de la clase
    #
    # El constructor unicamente inicializa la lista de Sujetos en la aplicacion
    def __init__(self):
        self.lista_de_sujetos = GestorSujeto()
        self.num_para_entrenar = None
        self.mean = None
        self.matriz_img_vec = None
        self.matriz_de_cov = None
        self.auto_valores = None
        self.auto_vectores = None
        self.pesos = None
    def agregar_sujeto(self, dict_sujeto):
        """## Metodo agregar_sujeto
    # @param dict_sujeto un diccionario con el nombre del sujeto y una lista con sus imagenes
    # @return True/False segun si se agrega con exito el sujeto"""
        return self.lista_de_sujetos.agregar(dict_sujeto)
    def cargar_imagenes(self, img_url, _num_para_entrenar=6):
        """## Metodo cargar_imagenes
    #
    # @param img_url la direccion local de donde se van a sacar los sujetos y sus imagenes
    # @return una tupla con informacion de si se realizo bien o mal
    # Ejm de una ruta valida:
    #C:/Users/HP/Desktop/TEC/II Semestre 2017/Aseguramiento de calidad/Proyecto/AutoCaras/Images"""
        self.num_para_entrenar = _num_para_entrenar
        try:
            # Se saca todos los nombres de carpetas en la ruta dada, estos pasan a ser
            #los nombres de los sujetos
            sujetos = [sujeto for sujeto in os.listdir(img_url)
                       if os.path.isdir(os.path.join(img_url, sujeto))]
            for sujeto in sujetos:
                #Ahora por cada sujeto se sacan los nombres de las imagenes en su respectiva carpeta
                imgspath = os.listdir(img_url + '/' + sujeto)
                dict_sujeto = {}
                dict_sujeto["nombre"] = sujeto
                dict_sujeto["fotos"] = []
                imgspath = imgspath[:_num_para_entrenar]
                for img in imgspath:
                    # Por ruta de imagen, la abrimos y transformamos la imagen
                    path = img_url + '/' + sujeto + '/' + img
                    #pylint: disable=maybe-no-member
                    #Se agrega esta instruccion debido a que pylint detecta que imread no es
                    #un miembro de cv2 cuando este si existe
                    arr = cv2.imread(path, 0) # Matriz de una imagen en escala de grises
                    #arr = cv2.resize(arr, (112, 92)) # Reescalamos la imagen para que sea 112*92
                    dict_sujeto["fotos"].append(arr)
                    # Se guarda el sujeto y sus imagenes en memoria
                    self.agregar_sujeto(dict_sujeto)
            return (0, "Carga completada!")
        except FileNotFoundError as fnf:
            print (fnf)
            return (-1, "Error: Direccion no encontrada")
        except Exception as excepcion: # pylint: disable-msg=W0703
            # pylint: disable-msg=C0301
            print ("El error '{0}' ha ocurrido. Argumentos {1}.".format(excepcion.message, excepcion.args))
            return (-1, "Error: Desconocido")
    def entrenar(self):
        """Genera una base de conocimiento contra la cual se van a comparar
        las imagenes a clasificar"""
        imgs = self.lista_de_sujetos.get_all_imgs()
        self.matriz_img_vec, self.mean = self.definir_matriz_de_imagenes(imgs)
        self.matriz_de_cov = self.definir_matriz_de_covarianza(self.matriz_img_vec)
        # pylint: disable-msg=C0301
        self.auto_valores, self.auto_vectores = self.definir_auto_valores_vectores(self.matriz_de_cov, self.matriz_img_vec)
        self.pesos = self.definir_pesos(self.matriz_img_vec, self.auto_vectores)
        # pylint: disable-msg=C0301
        #id = self.clasificar('C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images\\s36\\6.pgm',
        #self.mean, self.auto_vectores, self.pesos)
        #return self.lista_de_sujetos.get_sujeto_at(id)
    # pylint: disable=R0201
    def vectorizar_imagen(self, img):
        """##Funcion que vectoriza una imagen que le entra por parametro
    #@param img recibe la imagen
    #@return flat_img devuelve la lista de una imagen vectorizada."""
        flat_img = np.array(img, dtype='float64').flatten() # Vectorizacion de una matriz
        return flat_img
    def definir_matriz_de_imagenes(self, list_imgs):
        """    ##Funcion que crea la matriz con las imagenes vectorizadas
    #@param listImgs la lista de la imagen ya vectorizada
    #@return MatrizImgVec es la matriz con todas las imagenes vectorizadas de un sujeto"""
        total = len(list_imgs[0]) * len(list_imgs[0][0])
        numero_imagenes = len(list_imgs) #numero de imagenes a recorrer
        matriz_img_vec = np.empty(shape=(total, numero_imagenes), dtype='float64')
        #se crea la matriz que contendra las imagenes vectorizadas
        img_id = 0
        for training_img in list_imgs:
            img_vectorizada = self.vectorizar_imagen(training_img)
            matriz_img_vec[:, img_id] = img_vectorizada[:]
            img_id += 1
        mean_img = np.sum(matriz_img_vec, axis=1) / numero_imagenes
        for j in range(0, numero_imagenes):
            matriz_img_vec[:, j] -= mean_img[:]
        return (matriz_img_vec, mean_img)
    def definir_matriz_de_covarianza(self, matriz_img_vec):
        """    ## Metodo definir_matriz_de_covarianza
    #
    # @param matriz_img_vec el metodo recibe una matriz de imagenes vectorizadas
    #con la que se calculara la matriz de covarianza
    # @return matriz_cov se devuelve la matriz de covarianza calculada """
    #pylint: disable=maybe-no-member
        matriz_cov = np.matrix(matriz_img_vec.transpose()) * np.matrix(matriz_img_vec)
        np.divide(matriz_cov, len(matriz_img_vec[0]), out=matriz_cov, casting='unsafe')
        return matriz_cov
    def definir_auto_valores_vectores(self, matriz_cov, matriz_img_vec, _energia=0.85):
        """Recibe como parametros una matriz de covarianza junto a su respectiva matriz
        de imagenes vectorizadas"""
        auto_valores, auto_vectores = np.linalg.eig(matriz_cov)
        indices = auto_valores.argsort()[::-1]
        auto_valores = auto_valores[indices]
        auto_vectores = auto_vectores[indices]
        suma_autovalores = sum(auto_valores[:])
        contador_autovalores = 0
        informacion_en_autovalores = 0.0
        for auto_valor in auto_valores:
            contador_autovalores += 1
            informacion_en_autovalores += auto_valor / suma_autovalores
            if informacion_en_autovalores >= _energia:
                break
        auto_valores = auto_valores[0:contador_autovalores]
        auto_vectores = auto_vectores[0:contador_autovalores]
        auto_vectores = auto_vectores.transpose()
        auto_vectores = matriz_img_vec * auto_vectores
        norms = np.linalg.norm(auto_vectores, axis=0)
        auto_vectores = auto_vectores / norms
        return (auto_valores, auto_vectores)
    def definir_pesos(self, matriz_img_vec, auto_vectores):
        """Determina el peso de los autovectores. Recibe como parametros
        una matriz con imagenes vectorizdas y una matriz con sus respectivos autovectores"""
        return auto_vectores.transpose() * matriz_img_vec
    def clasificar(self, img_dir, mean, auto_vectores, pesos):
        """Recibe como parametros el directorio de la imagen a clasficar, la imagen media
        de las imagenes de entrenamiento, una matriz de autovectores y los pesos de estos"""
        #pylint: disable=maybe-no-member
        img = cv2.imread(img_dir, 0)
        img_col = np.array(img, dtype='float64').flatten()
        img_col -= mean
        img_col = np.reshape(img_col, (len(img_col), 1))
        autovectores_transpuesta = auto_vectores.transpose() * img_col
        diff = pesos - autovectores_transpuesta
        norms = np.linalg.norm(diff, axis=0)
        id_cercano = np.argmin(norms)
        return (id_cercano // self.num_para_entrenar) + 1
    