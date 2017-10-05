##@package docstring
#Created on Aug 16, 2017
#
#@author: Michael Choque
#@author: Nelson Gómez
#@author: William Espinoza

## Clase Sujeto
#
# Esta clase es la representacion abstracta de un sujeto
class Sujeto(object):

    ## Constructor de la clase
    # 
    # El constructor inicializa la lista de fotos de un sujeto y le asigna un nombre
    # @param nombre Nombre de un sujeto
    def __init__(self, nombre):
        self.nombre = nombre
        self.listaFotos = []
    
    ## Metodo AgregarFoto
    # 
    # Metodo simple de agregar a la lista de fotos una foto
    # @param foto matriz representando una imagen
    def AgregarFoto(self, foto):
        self.listaFotos.append(foto)
    
    ## Metodo GetListaFotos
    # 
    # Metodo get para la lista de fotos de un sujeto
    # @return una lista de matrices
    def GetListaFotos(self):
        return self.listaFotos
    
    def GetNombre(self):
        return self.nombre
    
    ## Metodo SetListaFotos
    # 
    # Metodo set para la lista de fotos un sujeto
    def SetListaFotos(self, listaFotos):
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