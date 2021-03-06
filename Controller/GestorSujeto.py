'''
Modulo encargado de gestion de sujetos y carga de sus respectivas imagenes

Created on Aug 16, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
'''
from Controller.GestorGeneral import GestorGeneral
from Model.Sujeto import Sujeto
class GestorSujeto(GestorGeneral):
    '''
    Clase GestorSujeto
    Clase hija del gestor general, encargada de guardar sujetos en memoria"
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
        Crea un nuevo sujeto y lo agrega a la lista_general de su padre
        @param dict_sujeto diccionario con el nombre y las fotos de un sujeto
        @return el retorno del Agregar de la clase padre
        """
        sujeto_nuevo = Sujeto(objeto["nombre"])
        sujeto_nuevo.set_lista_fotos(objeto["fotos"])
        return GestorGeneral.agregar(self, sujeto_nuevo)
    def get_all_imgs(self):
        '''
        Metodo get_all_imgs
        Metodo para sacar todas las imagenes de todos los sujetos guardados en memoria
        @return la lista con todas las imagenes
        '''
        lista_imagenes = []
        for sujeto in self.lista_general:
            lista_imagenes += sujeto.get_lista_fotos()
        return lista_imagenes
    def get_sujeto_at(self, id_sujeto):
        """Obtiene el sujeto almacenado en lista general al buscarlo por su numero de id
        Recibe como parametro un numero entero positivo
        @param el id del sujeto
        @return estado de la operacion"""
        contador = 0
        for sujeto in self.lista_general:
            #print("s: ", sujeto.get_nombre(), " ", contador, " - ", id_sujeto)
            if contador == id_sujeto-1:
                return (0, sujeto.get_nombre())
            contador += 1
        return (-1, "Sujeto no encontrado...")
    