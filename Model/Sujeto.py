'''
Clase utiizada para representar cada sujeto junto a su lista de fotografias

Created on Aug 16, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
'''


class Sujeto(object):
    """
    Clase Sujeto

    Esta clase es la representacion abstracta de un sujeto
    """
    def __init__(self, nombre):
        '''
        Constructor de la clase
        
        El constructor inicializa la lista de fotos de un sujeto y le asigna un nombre
        @param nombre Nombre de un sujeto
        '''
        self.nombre = nombre
        self.lista_fotos = []
    def agregar_foto(self, foto):
        '''
        Metodo agregar_foto

        Metodo simple de agregar a la lista de fotos una foto
        @param foto matriz representando una imagen
        '''
        self.listaFotos.append(foto)
    def get_lista_fotos(self):
        '''
        Metodo get_lista_fotos

        Metodo get para la lista de fotos de un sujeto
        @return una lista de matrices
        '''
        return self.listaFotos
    def get_nombre(self):
        return self.nombre
    def set_lista_fotos(self, listaFotos):
        '''
        Metodo set_lista_fotos
        
        Metodo set para la lista de fotos un sujeto
        '''
        self.listaFotos = listaFotos
    def __eq__(self, otro):
        '''
        Metodo __eq__

        Overwrite del metodo __eq__ de python, para poder hacer comparaciones segun nombre
        '''
        if otro is None:
            return False
        if not isinstance(otro, Sujeto):
            return False
        if not (otro.nombre == self.nombre):
            return False
        return True