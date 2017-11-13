'''
Created on Oct 8, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
'''
from Controller.Controlador import Controlador
class Facade(object):
    '''
    Clase Facade
    Esta clase permite separar la dependencia hacia el controlador
    '''
    def __init__(self):
        '''
        Constructor de la clase
        El constructor inicializa el controlador de la clase
        '''
        self.controlador = Controlador()
        self.controlador.carga_inicial()
    def cargar_imagenes(self, img_url, num_para_entrenar):
        '''
        Metodo cargar_imagenes
        Carga las imagenes para el entrenamiento
        @param img_url la direccion local de donde se van a sacar los sujetos y sus imagenes
        @return una tupla con informacion de si se realizo bien o mal
        '''
        if num_para_entrenar is None:
            return self.controlador.cargar_imagenes(img_url)
        return self.controlador.cargar_imagenes(img_url, _num_para_entrenar=num_para_entrenar)
    def entrenar(self, ent_prefix, energy_pct):
        '''
        Metodo entrenar
        Genera una base de conocimiento contra la cual se van a comparar
        las imagenes a clasificar
        @param un prefijo de como sera guardada la imagen y la cantidad de autovectores a conservar
        @return un numero que indica el estado y un mensaje
        '''
        return self.controlador.entrenar(ent_prefix, energy_pct)
    def clasificar(self, img_dir, ent_prefix, cargar_entrenamiento):
        '''
        Metodo clasificar
        Recibe como parametros el directorio de la imagen a clasficar, la imagen media
        de las imagenes de entrenamiento, una matriz de autovectores y los pesos de estos
        @param directorio de imagen a clasificar, la imagen media de las imagenes de entrenamiento
        @return sujeto clasificado
        '''
        sujeto_id = self.controlador.clasificar(img_dir, ent_prefix, cargar_entrenamiento)
        return self.controlador.lista_de_sujetos.get_sujeto_at(sujeto_id)
    def get_precision(self):
        """
        Metodo get_precision
        Carga un conjunto de muestras prueba midiendo presicion del sistema
        @param null
        @return null
        """
        return self.controlador.get_precision()
    