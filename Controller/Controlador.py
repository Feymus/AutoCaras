"""
Esta clase gestiona la interaccion entre la pagina web y el modelo
Gestiona el proceso de entrenamiento y clasificacion de sujetos

Created on Aug 16, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
"""
from __future__ import print_function
import os
import csv
import random
import ast
import cv2
import numpy as np
import tiempo
from Controller.GestorSujeto import GestorSujeto
from Controller.GestorEntrenamiento import GestorEntrenamiento
class Controlador(object):
    # pylint: disable=too-many-instance-attributes
    #se considera que los 10 atributos son necesarios
    '''
    Clase controlador
    Esta clase es la que permite la comunicacion entre los datos de la aplicacion
    y la interfaz de usuario
    '''
    def __init__(self):
        '''
        Constructor de la clase
        El constructor unicamente inicializa la lista de Sujetos en la aplicacion
        '''
        self.lista_de_sujetos = GestorSujeto()
        self.lista_entrenamientos = GestorEntrenamiento()
        self.num_para_entrenar = None
        self.mean = None
        self.matriz_img_vec = None
        self.matriz_de_cov = None
        self.auto_valores = None
        self.auto_vectores = None
        self.pesos = None
        self.de_entrenamiento = None
        self.num_sujetos = None
        self.url_sujetos = None
    def agregar_sujeto(self, dict_sujeto):
        '''
        Metodo agregar_sujeto
        Segun un diccionario que contiene al sujeto y sus imagenes, guarda al sujeto
        @param dict_sujeto un diccionario con el nombre del sujeto y una lista con sus imagenes
        @return True/False segun si se agrega con exito el sujeto
        '''
        return self.lista_de_sujetos.agregar(dict_sujeto)
    def seleccionar_imgs(self, cantidad):
        """
        Metodo seleccionar_imgs
        Seleccionar images a usar para entrenamiento de manera
        random
        @param cantidad, cantidad de imagenes a escoger
        @return imagenes seleccionadas
        """
        imgs_seleccionadas = random.sample(range(1, 11), cantidad)
        imgs_result = []
        for img in imgs_seleccionadas:
            imgs_result += [str(img) + ".pgm"]
        return imgs_result
    #@tiempo.measure_time
    def cargar_imagenes(self, img_url, _num_para_entrenar=6):
        """
        Metodo cargar_imagenes
        Carga las imagenes de los sujetos encontrados en cierta direccion, carga solo la cantidad
        especificada para entrenar
        @param img_url la direccion local de donde se van a sacar los sujetos y sus imagenes
        @return una tupla con informacion de si se realizo bien o mal
        Ejm de una ruta valida:
        C:/Users/HP/Desktop/TEC/II Semestre 2017/Aseguramiento de calidad/Proyecto/AutoCaras/Images
        """
        self.lista_de_sujetos = GestorSujeto()
        self.num_para_entrenar = _num_para_entrenar
        self.url_sujetos = img_url
        try:
            # Se saca todos los nombres de carpetas en la ruta dada, estos pasan a ser
            #los nombres de los sujetos
            sujetos = [sujeto for sujeto in os.listdir(img_url)
                       if os.path.isdir(os.path.join(img_url, sujeto))]
            self.num_sujetos = len(sujetos)
            #Ahora por cada sujeto se sacan los nombres de las imagenes en su respectiva carpeta
            imgspath = self.seleccionar_imgs(_num_para_entrenar)
            self.de_entrenamiento = imgspath
            for sujeto in sujetos:
                dict_sujeto = {}
                dict_sujeto["nombre"] = sujeto
                dict_sujeto["fotos"] = []
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
            # pylint: disable-msg=E1101
            print ("El error '{0}' ha ocurrido. Argumentos {1}.".format(excepcion.message,
                                                                         excepcion.args))
            return (-1, "Error: Desconocido")
    def entrenar(self, ent_prefix, energy_pct):
        """
        Metodo entrenar
        Genera una base de conocimiento contra la cual se van a comparar
        las imagenes a clasificar
        @param un prefijo de como sera guardada la imagen y la cantidad de autovectores a conservar
        @return un numero que indicar el estado y un mensaje
        """
        try:
            imgs = self.lista_de_sujetos.get_all_imgs()
            self.matriz_img_vec, self.mean = self.definir_matriz_de_imagenes(imgs)
            self.matriz_de_cov = self.definir_matriz_de_covarianza(self.matriz_img_vec)
            # pylint: disable-msg=C0301
            self.auto_valores, self.auto_vectores = self.definir_auto_valores_vectores(self.matriz_de_cov, self.matriz_img_vec, _energia=energy_pct)
            self.pesos = self.definir_pesos(self.matriz_img_vec, self.auto_vectores)
            # pylint: disable-msg=C0301
            if ent_prefix != "":
                self.guardar_entrenamiento(ent_prefix)
            else:
                self.guardar_entrenamiento("ent")
            return (0, "Entrenamiento completado!")
        except Exception as exception:# pylint: disable-msg=W0703
            # pylint: disable-msg=E1101
            print ("El error '{0}' ha ocurrido. Argumentos {1}.".format(exception.message,
                                                                         exception.args))
            return (-1, "Error: Desconocido")
    # pylint: disable=R0201
    def vectorizar_imagen(self, img):
        """
        Metodo vectorizar_imagen
        Funcion que vectoriza una imagen que le entra por parametro
        @param img recibe la imagen
        @return flat_img devuelve la lista de una imagen vectorizada
        """
        flat_img = np.array(img, dtype='float64').flatten() # Vectorizacion de una matriz
        return flat_img
    def definir_matriz_de_imagenes(self, list_imgs):
        """
        Metodo definir_matriz_de_imagenes
        Funcion que crea la matriz con las imagenes vectorizadas
        @param listImgs la lista de la imagen ya vectorizada
        @return MatrizImgVec es la matriz con todas las imagenes vectorizadas de un sujeto
        """
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
        """
        Metodo definir_matriz_de_covarianza
        Genera la matri de covarianza segun la matriz de imagenes y su transpuesta
        @param matriz_img_vec el metodo recibe una matriz de imagenes vectorizadas
        con la que se calculara la matriz de covarianza
        @return matriz_cov se devuelve la matriz de covarianza calculada
        """
        #pylint: disable=maybe-no-member
        matriz_cov = np.matrix(matriz_img_vec.transpose()) * np.matrix(matriz_img_vec)
        np.divide(matriz_cov, len(matriz_img_vec[0]), out=matriz_cov, casting='unsafe')
        return matriz_cov
    def definir_auto_valores_vectores(self, matriz_cov, matriz_img_vec, _energia=0.85):
        """
        Metodo definir_auto_valores_vectores
        Recibe como parametros una matriz de covarianza junto a su respectiva matriz
        de imagenes vectorizadas
        @param matriz de covarianza, matriz de imagenes vectorizadas
        y cantidad de autovectores a conservar
        @return tupla con autovalores y autovectores
        """
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
        """
        Metodo definir_pesos
        Determina el peso de los autovectores (imagenes proyectadas). Recibe como parametros
        una matriz con imagenes vectorizdas y una matriz con sus respectivos autovectores
        @param matriz de imagenes vectorizadas, auto vectores
        @return el peso
        """
        return auto_vectores.transpose() * matriz_img_vec
    def clasificar(self, img_dir, ent_prefix, cargar_entrenamiento):
        """
        Metodo clasificar
        Recibe como parametros el directorio de la imagen a clasficar, la imagen media
        de las imagenes de entrenamiento, una matriz de autovectores y los pesos de estos
        @param directorio de imagen a clasificar, la imagen media de las imagenes de entrenamiento
        @return id_cercano
        """
        #pylint: disable=maybe-no-member
        if cargar_entrenamiento is True:
            self.cargar_entrenamiento(ent_prefix)
        img = cv2.imread(img_dir, 0)
        img_col = np.array(img, dtype='float64').flatten()
        img_col -= self.mean
        img_col = np.reshape(img_col, (len(img_col), 1))
        autovectores_transpuesta = self.auto_vectores.transpose() * img_col
        diff = self.pesos - autovectores_transpuesta
        norms = np.linalg.norm(diff, axis=0)
        id_cercano = np.argmin(norms)
        return (id_cercano // self.num_para_entrenar) + 1
    def guardar_entrenamiento(self, ent_prefix):
        '''
        Metodo guardar_entrenamiento
        Guarda el sujeto que se entreno en el sistema
        @param el prefijo que fue escrito
        @return ...
        '''
        entrenamiento = {}
        nbr_auto_vectores = ent_prefix + "_auto_caras.txt"
        np.savetxt('../datos/entrenamientos/' + nbr_auto_vectores, self.auto_vectores)
        entrenamiento["auto_vectores"] = self.auto_vectores
        nbr_mean = ent_prefix + "_mean.txt"
        np.savetxt('../datos/entrenamientos/' + nbr_mean, self.mean)
        entrenamiento["mean"] = self.mean
        nbr_pesos = ent_prefix + "_proyecciones.txt"
        np.savetxt('../datos/entrenamientos/' + nbr_pesos, self.pesos)
        entrenamiento["pesos"] = self.pesos
        with open('../datos/entrenamientos/' + ent_prefix + "_imgs.txt", "w+") as file:
            file.write(str(self.de_entrenamiento))
        file.close()
        entrenamiento["imgs_usadas"] = self.de_entrenamiento
        entrenamiento["prefijo"] = ent_prefix
        self.lista_entrenamientos.agregar(entrenamiento)
    def cargar_entrenamiento(self, ent_prefix):
        """
        Metodo cargar_entrenamiento
        Toma los datos de los archivos .txt y los pone en sus respectivas variables
        @param el prefijo
        @return ...
        """
        if ent_prefix != "":
            entrenamiento = self.lista_entrenamientos.cargar_entrenamiento(ent_prefix)
        else:
            entrenamiento = self.lista_entrenamientos.cargar_entrenamiento("ent")
        
        self.auto_vectores = entrenamiento[0]
        self.mean = entrenamiento[1]
        self.pesos = entrenamiento[2]
        self.de_entrenamiento = entrenamiento[3]
        self.num_para_entrenar = len(self.de_entrenamiento)
    def carga_inicial(self):
        """
        Metodo carga_inicial
        Carga todos los entrenamientos guardados en la carpeta entrenamientos
        """
        prefijos = self.get_prefijos()
        for prefijo in prefijos:
            entrenamiento = {}
            nbr_auto_vectores = prefijo + "_auto_caras.txt"
            entrenamiento["auto_vectores"] = np.matrix(np.loadtxt('../datos/entrenamientos/'
                                                       + nbr_auto_vectores, dtype='float64'))
            nbr_mean = prefijo + "_mean.txt"
            entrenamiento["mean"] = np.loadtxt('../datos/entrenamientos/'
                                                + nbr_mean, dtype='float64')
            nbr_pesos = prefijo + "_proyecciones.txt"
            entrenamiento["pesos"] = np.matrix(np.loadtxt('../datos/entrenamientos/'
                                                           + nbr_pesos, dtype='float64'))
            with open('../datos/entrenamientos/' + prefijo + "_imgs.txt", "r") as file:
                data = file.read()
                entrenamiento["imgs_usadas"] = ast.literal_eval(data)
            entrenamiento["prefijo"] = prefijo
            self.lista_entrenamientos.agregar(entrenamiento)
    def get_prefijos(self):
        """
        Metodo get_prefijos
        Obtiene los prefijos de los entrenamientos guardados
        @return lista con los prefijos
        """
        entrenamientos_url = '../datos/entrenamientos/'
        prefijos_tmp = [prefijo for prefijo in os.listdir(entrenamientos_url)]
        prefijos = []
        for prefijo in prefijos_tmp:
            prefijo = prefijo.replace("_auto_caras.txt", "")
            prefijo = prefijo.replace("_mean.txt", "")
            prefijo = prefijo.replace("_proyecciones.txt", "")
            prefijo = prefijo.replace("_imgs.txt", "")
            if (prefijo in prefijos) is False:
                prefijos += [prefijo]
        return prefijos
    # pylint: disable=R0914
    def get_precision(self):
        """
        Metodo get_precision
        Carga un conjunto de muestras prueba midiendo presicion del sistema
        @param null
        @return null
        """
        try:
            file = open("../datos/pruebas/precision.csv", 'wt')
            writer = csv.writer(file, lineterminator='\n')
            sujetos = [sujeto for sujeto in os.listdir(self.url_sujetos)
                           if os.path.isdir(os.path.join(self.url_sujetos, sujeto))]
            tabla_de_clases = self.armar_tabla_de_clases(sujetos)
            for sujeto in sujetos:
                imgspath_entrenamiento = self.de_entrenamiento
                imgspath_pruebas = os.listdir(self.url_sujetos + '/' + sujeto)
                for img in imgspath_pruebas:
                    if (img in imgspath_entrenamiento) is False:
                        path = self.url_sujetos + '/' + sujeto + '/' + img
                        id_resultante = self.clasificar(path, "PRUEBAS", False)
                        sujeto_resultante = self.lista_de_sujetos.get_sujeto_at(id_resultante)
                        tabla_de_clases = self.agregar_a_tabla(tabla_de_clases,
                                                                sujeto_resultante[1], sujeto)
            cant_sujetos = 0
            avg_precision = 0
            avg_recall = 0
            for sujeto in sujetos:
                cant_sujetos += 1
                result = self.evaluacion_de_clase(tabla_de_clases, sujeto)
                precision = result[0]
                avg_precision += precision
                recall = result[1]
                avg_recall += recall
                falsos_n = result[2]
                falsos_p = result[3]
                verdaderos_p = result[4]
                writer.writerow(('Sujeto', sujeto))
                writer.writerow(('Precision', precision))
                writer.writerow(('Recall', recall))
                writer.writerow(('Falsos positivos', falsos_n))
                writer.writerow(('Falsos negativos', falsos_p))
                writer.writerow(('Verdaderos positivos', verdaderos_p))
                writer.writerow((''))
            avg_precision = avg_precision / cant_sujetos
            avg_recall = avg_recall / cant_sujetos
            writer.writerow(('Precision promedio', avg_precision))
            writer.writerow(('Recall promedio', avg_recall))
            writer.writerow((''))
            file.close()
            return (0, "Precision de cada sujeto generada exitosamente!")
        except Exception as exception: # pylint: disable-msg=W0703
            # pylint: disable-msg=E1101
            print ("El error '{0}' ha ocurrido. Argumentos {1}.".format(exception.message,
                                                                         exception.args))
            return (-1, "Error: Desconocido")
    def armar_tabla_de_clases(self, sujetos):
        """
        Metodo armar_tabla_de_clases
        Arma la tabla de clases
        @param sujetos
        @return tabla de clases
        """
        tabla_de_clases = [[0]]
        for sujeto in sujetos:
            tabla_de_clases[0] += [sujeto]
            tabla_de_clases += [[sujeto] + [0] * len(sujetos)]
        return tabla_de_clases
    def agregar_a_tabla(self, tabla, sujeto_clasificado, sujeto_verdadero):
        """
        Metodo agregar_a_tabla
        Agrega a la tabla de falsos positivos y negavitos un nuevo valor
        @param sujeto clasificado y sujeto verdadero
        @return la tabla
        """
        encontrado = False
        for fila in range(1, len(tabla)):
            if tabla[fila][0] == sujeto_clasificado:
                for columna in range(1, len(tabla[0])):
                    if tabla[0][columna] == sujeto_verdadero:
                        tabla[fila][columna] += 1
                        encontrado = True
                        break
            if encontrado is True:
                break
        return tabla
    def evaluacion_de_clase(self, tabla, sujeto):
        """
        Metodo evaluacion_de_clase
        Evalua la tabla respecto a los sujetos
        @param la tabla y los sujetos
        @return el resultado de la tabla
        """
        encontrado = False
        precision = 0
        recall = 0
        for fila in range(1, len(tabla)):
            if tabla[fila][0] == sujeto:
                for columna in range(1, len(tabla[0])):
                    if tabla[0][columna] == sujeto:
                        verdaderos_positivos = tabla[fila][columna]
                        falsos_positivos = self.get_falsos_positivos(tabla, fila, columna)
                        falsos_negativos = self.get_falsos_negativos(tabla, fila, columna)
                        encontrado = True
                        break
            if encontrado is True:
                break
        if verdaderos_positivos + falsos_positivos != 0:
            precision = 100 * verdaderos_positivos / (verdaderos_positivos + falsos_positivos)
        if verdaderos_positivos + falsos_negativos != 0:
            recall = 100 * verdaderos_positivos / (verdaderos_positivos + falsos_negativos)
        return (precision, recall, falsos_positivos, falsos_negativos, verdaderos_positivos)
    def get_falsos_positivos(self, tabla, fila, columna):
        """
        Metodo get_falsos_positivos
        Obtiene los falsos positivos
        @param la tabla, el numero de la fila y columna
        @return los falsos positivos
        """
        falsos_positivos = 0
        for ccolumna in range(1, len(tabla[0])):
            if ccolumna != columna:
                falsos_positivos += tabla[fila][ccolumna]
        return falsos_positivos
    def get_falsos_negativos(self, tabla, fila, columna):
        """
        Metodo get_falsos_negativos
        Obtiene los falsos negativos
        @param tabla, el numero de la fila y columna
        @return  falsos negativos
        """
        falsos_negativos = 0
        for ffila in range(1, len(tabla)):
            if ffila != fila:
                falsos_negativos += tabla[ffila][columna]
        return falsos_negativos
    
