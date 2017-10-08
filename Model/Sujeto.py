"Clase utiizada para representar cada sujeto junto a su lista de fotografias"
#Created on Aug 16, 2017
#
#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza


class Sujeto(object):
    """## Clase Sujeto
#
# Esta clase es la representacion abstracta de un sujeto"""
    ## Constructor de la clase
    #
    # El constructor inicializa la lista de fotos de un sujeto y le asigna un nombre
    # @param nombre Nombre de un sujeto
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_fotos = []
    ## Metodo agregar_foto
    #
    # Metodo simple de agregar a la lista de fotos una foto
    # @param foto matriz representando una imagen
    def agregar_foto(self, foto):
        self.listaFotos.append(foto)
    
    ## Metodo get_lista_fotos
    # 
    # Metodo get para la lista de fotos de un sujeto
    # @return una lista de matrices
    def get_lista_fotos(self):
        return self.listaFotos
    
    def get_nombre(self):
        return self.nombre
    
    ## Metodo set_lista_fotos
    # 
    # Metodo set para la lista de fotos un sujeto
    def set_lista_fotos(self, listaFotos):
        self.listaFotos = listaFotos
    
    ## Metodo __eq__
    # 
    # Overwrite del metodo __eq__ de python, para poder hacer comparaciones segun nombre
    def __eq__(self, otro):
        if otro is None:
            return False
        if not isinstance(otro, Sujeto):
            return False
        if not (otro.nombre == self.nombre):
            return False
        return True