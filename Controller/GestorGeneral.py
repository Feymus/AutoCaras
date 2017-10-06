"Clase madre a partir de la cual heredan los demas gestores. Contiene las operaciones basicas CRUD"
#Created on Aug 16, 2017

#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza


## Clase GestorGeneral
#

class GestorGeneral(object):
    "Esta clase es utilizada para el gestion de las listas del controlador"
    ## Constructor de la clase
    #
    # Inicializa la lista de objetos a guardar
    def __init__(self):
        self.lista_general = []
    def agregar(self, objeto):
        """ Metodo Agregar
     Metodo simple de agregar a una lista, antes consulta si el objeto ya habia sido agregado antes
     @param objeto un objeto cuaquiera para guardar en la lista
     @return True/False dependiendo de si el objeto ya habia sido agregado o no"""
        if self.consultar(objeto) is None:
            self.lista_general.append(objeto)
            return True
        return False
    def consultar(self, objeto):
        """Metodo Consultar
    # Metodo para consultar un objeto existente en memoria
    # @param objeto puede ser una instancia de un objeto con el valor primario
    # con el que se buscara el objeto en la lista
    # @return objeto encontrado o por el contrario None"""
        if objeto in self.lista_general:
            pos = self.lista_general.index(objeto)
            return self.lista_general[pos]
        return None
    def eliminar(self, objeto):
        """## Metodo Eliminar
    #
    # Metodo para eliminar un objeto en la listaGeneral
    # @param objeto puede ser una instancia de un objeto con el valor primaria con
    el que se buscara el objeto en la lista
    # @return True/False segun si el objeto existe o no (antes de ser eliminado)"""
        if not self.consultar(objeto) is None:
            self.lista_general.remove(objeto)
            return True
        return False

    def modificar(self, objeto):
        """## Metodo Modificar
    # Metodo para modificar un objeto
    # @param objeto puede ser una instancia de un objeto con el valor
    primaria con el que se buscara el objeto en la lista
    # @return True/False segun si el objeto existe o no (antes de modificarlo)"""
        if objeto in self.lista_general:
            pos = self.lista_general.index(objeto)
            self.lista_general[pos] = objeto
            return True
        return False
    def get_lista_general(self):
        """## Metodo GetListaGeneral
    #
    # Metodo get para devolver la lista general
    # @return La lista de objetos que han sido guardados"""
        return self.lista_general
    