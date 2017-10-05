##
#Created on Aug 16, 2017
#
#@author: Michael Choque
#@author: Nelson Gómez
#@author: William Espinoza

from Controller.GestorGeneral import GestorGeneral
from Model.Sujeto import Sujeto

## Clase GestorSujeto
#
# Clase hija del gestor general, encargada de guardar sujetos en memoria
class GestorSujeto(GestorGeneral):


    ## Constructor de la clase
    #
    # El constructor solo llama a su constructor padre
    def __init__(self):
        GestorGeneral.__init__(self)
    
    ## Metodo Agregar
    # 
    # Crea un nuevo sujeto y lo agrega a la listaGeneral de su padre
    # @param dict_sujeto diccionario con el nombre y las fotos de un sujeto
    # @return el retorno del Agregar de la clase padre
    def Agregar(self, dict_sujeto):
        sujeto_nuevo = Sujeto(dict_sujeto["nombre"])
        sujeto_nuevo.SetListaFotos(dict_sujeto["fotos"])
        return GestorGeneral.Agregar(self, sujeto_nuevo)
    
    ## Metodo getAllImgs
    #
    # Metodo para sacar todas las imagenes de todos los sujetos guardados en memoria
    # @return la lista con todas las imagenes
    def getAllImgs(self):
        listaImagenes = []
        
        for sujeto in self.listaGeneral:
            listaImagenes += sujeto.GetListaFotos()
            
        return listaImagenes
    
    def GetSujetoAt(self, id):
        contador = 0
        for sujeto in self.listaGeneral:

            if(contador == id-1):
                print("Si, ", contador, " - ", sujeto.GetNombre())
            else:
                print("No, ", contador, " - ", sujeto.GetNombre())
            contador += 1
        