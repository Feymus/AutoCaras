#Created on Oct 8, 2017
#
#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza
from Controller.Controlador import Controlador

class Facade(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        self.controlador = Controlador()
        
    
    def entrenar(self, img_url, _num_para_entrenar=6):
        result = self.controlador.cargar_imagenes(img_url, _num_para_entrenar)
        if(result[0] != 0):
            return result
        entrenamiento_result = self.controlador.entrenar()
        if(entrenamiento_result[0] != 0):
            return entrenamiento_result
        return result
    
    def clasificar(self):
        pass