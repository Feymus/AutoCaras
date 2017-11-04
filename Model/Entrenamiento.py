'''
Created on Nov 3, 2017

@author: HP
'''

class Entrenamiento(object):
    '''
    Clase Entrenamiento
    Esta clase es la representacion abstracta de un entrenamiento
    '''
    def __init__(self, dict_entrenamiento):
        '''
        Constructor de la clase
        El constructor guarda lo necesario para realizar la clasificacion
        @param auto_vectores, los auto vectores en el entrenamiento
        @param mean, la cara promedio
        @param pesos, las imagenes proyectadas
        @param imgs_usadas, las imagenes usadas para entrenar
        '''
        self.auto_vectores = dict_entrenamiento["auto_vectores"]
        self.mean = dict_entrenamiento["mean"]
        self.pesos = dict_entrenamiento["pesos"]
        self.imgs = dict_entrenamiento["imgs_usadas"]
        self.prefijo = dict_entrenamiento["prefijo"]
    def get_entrenamiento(self):
        """
        Metodo get_entrenamiento
        Metodo simple que regresa todos sus atributos para la carga
        del entrenamiento
        @param null
        """
        return (self.auto_vectores, self.mean, self.pesos, self.imgs)
    def get_prefijo(self):
        """
        Metodo get_prefijo
        Metodo que devuelve el prefijo del entrenamiento
        @return el prefijo
        """
        return self.prefijo
    