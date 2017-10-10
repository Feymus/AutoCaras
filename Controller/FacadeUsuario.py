'''
Created on Oct 9, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
'''
from Controller.Facade import Facade
class FacadeUsuario(Facade):
    '''
    Clase FacadeUsuario
    
    Esta clase permite separar los funciones que puede realizar un usuario comun de un operador
    '''
    def __init__(self, p_facade):
        '''
        Costructor de clase
        
        El constructor inicializa el facade de la clase
        '''
        self.facade = p_facade
    def clasificar(self, img_dir, ent_prefix, cargar_entrenamiento):
        '''
        Metodo clasificar
        
        Recibe como parametros el directorio de la imagen a clasficar, la imagen media
        de las imagenes de entrenamiento, una matriz de autovectores y los pesos de estos
        
        @param directorio de imagen a clasificar, la imagen media de las imagenes de entrenamiento
        @return id_cercano
        '''
        return self.facade.clasificar(img_dir, ent_prefix, cargar_entrenamiento)