'''
Created on Oct 9, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
'''
from Controller.Facade import Facade
class FacadeOperador(Facade):
    '''
    Clase FacadeOperador
    Esta clase permite separar los funciones que puede realizar un operador de un usuario comun
    '''
    #pylint: disable=W0231
    def __init__(self, p_facade):
        '''
        Costructor de clase
        El constructor inicializa el facade de la clase
        '''
        self.facade = p_facade
    def cargar_imagenes(self, img_url, num_para_entrenar):
        '''
        Metodo cargar_imagenes
        Carga las imagenes para el entrenamiento
        @param img_url la direccion local de donde se van a sacar los sujetos y sus imagenes
        @return una tupla con informacion de si se realizo bien o mal
        '''
        return self.facade.cargar_imagenes(img_url, num_para_entrenar)
    def entrenar(self, ent_prefix, energy_pct):
        '''
        Metodo entrenar
        Genera una base de conocimiento contra la cual se van a comparar
        las imagenes a clasificar
        @param un prefijo de como sera guardada la imagen y la cantidad de autovectores a conservar
        @return un numero que indica el estado y un mensaje
        '''
        return self.facade.entrenar(ent_prefix, energy_pct)
    def get_precision(self):
        """
        Metodo get_precision
        Carga un conjunto de muestras prueba midiendo presicion del sistema
        @param null
        @return null
        """
        return self.facade.get_precision()
    