'''
Created on Nov 3, 2017

@author: HP
'''
from Controller.GestorGeneral import GestorGeneral
from Model.Entrenamiento import Entrenamiento
class GestorEntrenamiento(GestorGeneral):
    '''
    Clase GestorEntrenamiento
    Clase hija del gestor general, encargada de guardar entrenamientos en memoria
    '''
    def __init__(self):
        '''
        Constructor de la clase
        El constructor solo llama a su constructor padre
        '''
        GestorGeneral.__init__(self)
    def agregar(self, objeto):
        """
        Metodo Agregar
        Crea un nuevo entrenamiento y lo agrega a la lista_general de su padre
        @param dict_entrenamiento diccionario con los datos del nuevo entrenamiento
        @return el retorno del Agregar de la clase padre
        """
        entrenamiento = Entrenamiento(objeto)
        return GestorGeneral.agregar(self, entrenamiento)
    def cargar_entrenamiento(self, prefijo):
        """
        Metodo cargar_entrenamiento
        Regresa el entrenamiento que tenga tal prefijo
        @param prefijo, nombre del entrenamiento a cargar
        @return los valores importantes del entrenamiento
        """
        for entrenamiento in self.lista_general:
            if entrenamiento.get_prefijo() == prefijo:
                return entrenamiento.get_entrenamiento()
        return (-1, "Entrenamiento no encontrado...")
    