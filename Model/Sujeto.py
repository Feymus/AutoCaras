'''
Created on Aug 16, 2017

@author: HP
'''

class Sujeto(object):
    '''
    classdocs
    '''

    def __init__(self, nombre):
        self.nombre = nombre
        self.listaFotos = []
        
    def AgregarFoto(self, foto):
        self.listaFotos.append(foto)
        
    def GetListaFotos(self):
        return self.listaFotos
    
    def SetListaFotos(self, listaFotos):
        self.listaFotos = listaFotos
    
    def __eq__(self, otro):
        if otro is None:
            return False
        if not isinstance(otro, Sujeto):
            return False
        if not (otro.nombre == self.nombre):
            return False
        return True