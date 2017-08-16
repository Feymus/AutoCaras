'''
Created on Aug 16, 2017

@author: HP
'''

class GestorGeneral(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.listaGeneral = []
    
    def Agregar(self, objeto):
        if self.Consultar(objeto) == None:
            self.listaGeneral.append(objeto)
            return True
        return False
        
    def Consultar(self, objeto):
        if objeto in self.listaGeneral:
            pos = self.listaGeneral.index(objeto)
            return self.listaGeneral[pos]
        return None
    
    def Eliminar(self, objeto):
        if not self.Consultar(objeto) == None:
            self.listaGeneral.remove(objeto)
            return True
        return False
    
    def Modificar(self, objeto):
        if objeto in self.listaGeneral:
            pos = self.listaGeneral.index(objeto)
            self.listaGeneral[pos] = objeto
            return True
        return False
    
    def GetListaGeneral(self):
        return self.listaGeneral