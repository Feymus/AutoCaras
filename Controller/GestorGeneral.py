##@package docstring
#Created on Aug 16, 2017
#
#@author: Michael Choque
#@author: Nelson Gómez
#@author: William Espinoza


## Clase GestorGeneral
#
# Esta clase es utilizada para el gestion de las listas del controlador
class GestorGeneral(object):

    ## Constructor de la clase 
    #
    # Inicializa la lista de objetos a guardar
    def __init__(self):
        self.listaGeneral = []
    
    ## Metodo Agregar
    #
    # Metodo simple de agregar a una lista, antes consulta si el objeto ya habia sido agregado antes
    # @param objeto un objeto cuaquiera para guardar en la lista
    # @return True/False dependiendo de si el objeto ya habia sido agregado o no
    def Agregar(self, objeto):
        if self.Consultar(objeto) == None:
            self.listaGeneral.append(objeto)
            return True
        return False
    
    ## Metodo Consultar
    #
    # Metodo para consultar un objeto existente en memoria
    # @param objeto puede ser una instancia de un objeto con el valor primaria con el que se buscara el objeto en la lista
    # @return objeto encontrado o por el contrario None
    def Consultar(self, objeto):
        if objeto in self.listaGeneral:
            pos = self.listaGeneral.index(objeto)
            return self.listaGeneral[pos]
        return None
    
    ## Metodo Eliminar
    #
    # Metodo para eliminar un objeto en la listaGeneral
    # @param objeto puede ser una instancia de un objeto con el valor primaria con el que se buscara el objeto en la lista
    # @return True/False segun si el objeto existe o no (antes de ser eliminado)
    def Eliminar(self, objeto):
        if not self.Consultar(objeto) == None:
            self.listaGeneral.remove(objeto)
            return True
        return False
    
    ## Metodo Modificar
    #
    # Metodo para modificar un objeto
    # @param objeto puede ser una instancia de un objeto con el valor primaria con el que se buscara el objeto en la lista
    # @return True/False segun si el objeto existe o no (antes de modificarlo)
    def Modificar(self, objeto):
        if objeto in self.listaGeneral:
            pos = self.listaGeneral.index(objeto)
            self.listaGeneral[pos] = objeto
            return True
        return False
    
    ## Metodo GetListaGeneral
    #
    # Metodo get para devolver la lista general
    # @return La lista de objetos que han sido guardados
    def GetListaGeneral(self):
        return self.listaGeneral