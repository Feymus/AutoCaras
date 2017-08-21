##@package docstring
#Created on Aug 19, 2017
#
#@author: Michael Choque
#@author: Nelson Gómez
#@author: William Espinoza

import unittest
from Controller.Controlador import Controlador

## Clase ControladorTest
#
# Esta clase controla lo que tiene que ver con pruebas unitarias de la clase Controlador
class ControladorTest(unittest.TestCase):

    ## Metodo setUp
    #
    # El metodo setUp inicializa todo lo necesario para realizar las pruebas
    def setUp(self):
        self.foo = Controlador()

    
    ## Metodo test_CargarImagenes
    #
    # Prueba del metodo CargarImagenes en la clase Controlador, la prueba se realiza asegurando que se consigan todas las imagenes de los sujetos
    # que esten en la direccion dada y confirmando que la lista de sujetos no este vacia y que existan imagenes (esto ultimo puede no darse)
    def test_CargarImagenes(self):
        result = self.foo.CargarImagenes("../Images/")
        self.assertEqual(result[0], 0)
        self.assertNotEqual(self.foo.listaDeSujetos.getAllImgs(), [])
        self.assertNotEqual(self.foo.listaDeSujetos.listaGeneral, [])

    ## Metodo test_VectorizarImagen
    #
    # Prueba del metodo VectorizarImagen en la clase Controlador, la prueba se realiza asegurando que la imagen tenga el tamano correcto
    # y confirmando el primer y ultimo pixel de a imagen (los cuales pueden variar un poco por las transformacinoes)
    def test_VectorizarImagen(self):
        self.foo.CargarImagenes("../Images/")
        imagenes = self.foo.listaDeSujetos.getAllImgs()
        result = self.foo.VectorizarImagen(imagenes[0])
        self.assertEqual(len(result), 10304)
        self.assertGreaterEqual(result[0], 0)
        self.assertLessEqual(result[0], 255)
        self.assertGreaterEqual(result[-1], 0)
        self.assertLessEqual(result[-1], 255)
    
    ## Metodo test_MatrizDeImagenes
    #
    # Prueba del metodo DefinirMatrizDeImagenes en la case Controlador, la prueba se realiza asegurando el tamano de la matriz (tanto filas como columnas)
    # segun la cantidad de imagenes
    def test_MatrizDeImagenes(self):
        self.foo.CargarImagenes("../Images/")
        imagenes = self.foo.listaDeSujetos.getAllImgs()
        result = self.foo.DefinirMatrizDeImagenes(imagenes)
        self.assertEquals(len(result), 10304)
        self.assertEquals(len(result[0]), 410)
    
    ## Metodo test_MatrizDeCovarianza
    #
    # Prueba del metodo DefinirMatrizDeCovarianza en la case Controlador, la prueba se realiza asegurando el tamano de la matriz (tanto filas como columnas)
    # segun la cantidad de imagenes, la cual siempre debera de ser 10304*10304
    def test_MatrizDeCovarianza(self):
        self.foo.CargarImagenes("../Images/")
        imagenes = self.foo.listaDeSujetos.getAllImgs()
        matrizImgVec = self.foo.DefinirMatrizDeImagenes(imagenes)
        result = self.foo.DefinirMatrizDeCovarianza(matrizImgVec)
        self.assertEquals(len(result), 10304)
        self.assertEquals(len(result[0]), 10304)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()