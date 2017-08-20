'''
Created on Aug 16, 2017

@author: HP
'''
from Controller.GestorGeneral import GestorGeneral
from Model.Sujeto import Sujeto


class GestorSujeto(GestorGeneral):
    '''
    classdocs
    '''


    def __init__(self):
        GestorGeneral.__init__(self)
        
    def Agregar(self, dict_sujeto):
        sujeto_nuevo = Sujeto(dict_sujeto["nombre"])
        sujeto_nuevo.SetListaFotos(dict_sujeto["fotos"])
        return GestorGeneral.Agregar(self, sujeto_nuevo)
    
    def getAllImgs(self):
        listaImagenes = []
        
        for sujeto in self.listaGeneral:
            listaImagenes += sujeto.GetListaFotos()
            
        return listaImagenes
        