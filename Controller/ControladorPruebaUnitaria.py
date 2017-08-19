##@package docstring
#Created on Aug 19, 2017
#
#@author: Michael Choque

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


    def tearDown(self):
        pass

    ## Metodo test_VectorizarImagen
    #
    # Prueba del metodo VectorizarImagen en la clase Controlador, la prueba se realiza asegurando que la imagen tenga el tamano correcto
    # y confirmando el primer y ultimo pixel de a imagen (los cuales pueden variar un poco por las transformacinoes)
    def test_VectorizarImagen(self):
        result = self.foo.VectorizarImagen("../Images/s1/1.pgm")
        self.assertEqual(len(result), 10304)
        self.assertAlmostEquals(result[0], 131)
        self.assertAlmostEquals(result[-1], 25)
    
    ## Metodo test_MatrizDeImagenes
    #
    # Prueba del metodo DefinirMatrizDeImagenes en la case Controlador, la prueba se realiza asegurando el tamano de la matriz (tanto filas como columnas)
    # segun la cantidad de imagenes
    def test_MatrizDeImagenes(self):
        result = self.foo.DefinirMatrizDeImagenes(["../Images/s1/1.pgm", "../Images/s1/2.pgm"])
        self.assertEquals(len(result), 10304)
        self.assertEquals(len(result[0]), 2)
    
    ## Metodo test_MatrizDeCovarianza
    #
    # Prueba del metodo DefinirMatrizDeCovarianza en la case Controlador, la prueba se realiza asegurando el tamano de la matriz (tanto filas como columnas)
    # segun la cantidad de imagenes, la cual siempre debera de ser 10304*10304
    def test_MatrizDeCovarianza(self):
        matrizImgVec = self.foo.DefinirMatrizDeImagenes(["../Images/s1/1.pgm", "../Images/s1/2.pgm", "../Images/s1/3.pgm"])
        result = self.foo.DefinirMatrizDeCovarianza(matrizImgVec)
        self.assertEquals(len(result), 10304)
        self.assertEquals(len(result[0]), 10304)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()