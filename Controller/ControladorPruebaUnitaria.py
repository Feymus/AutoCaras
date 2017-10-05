##@package docstring
#Created on Aug 19, 2017
#
#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza

import unittest
from Controller.Controlador import Controlador
import numpy as np

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
    # Prueba del metodo VectorizarImagen en la clase Controlador, la prueba se realiza asegurando que la imagen se haya aplanado a 1 dimension
    # y confirmando el tamano final de la imagen
    def test_VectorizarImagen(self):
        result = self.foo.VectorizarImagen([[1,2],[3,4]])
        lista_resultado = np.array([1,2,3,4], dtype='float64')
        self.assertEqual(result.tolist(), lista_resultado.tolist())
        self.assertEqual(len(result), 4)

    
    ## Metodo test_MatrizDeImagenes
    #
    # Prueba del metodo DefinirMatrizDeImagenes en la case Controlador, la prueba se realiza asegurando el resultado de la matriz
    # segun una lista de "imagenes"
    def test_MatrizDeImagenes(self):
        imagenes = [[[1,3]],[[20,40]]]
        result, mean = self.foo.DefinirMatrizDeImagenes(imagenes)
        self.assertEquals(result.tolist(), [[-9.5, 9.5], [-18.5, 18.5]])
        self.assertEquals(mean.tolist(), [10.5, 21.5])

    
    ## Metodo test_MatrizDeCovarianza
    #
    # Prueba del metodo DefinirMatrizDeCovarianza en la case Controlador, la prueba se realiza asegurando el resultado de la matriz
    # segun la cantidad de "imagenes"
    def test_MatrizDeCovarianza(self):
        result = self.foo.DefinirMatrizDeCovarianza(np.matrix([[-9.5, 9.5], [-18.5, 18.5]]))
        self.assertEquals(result.tolist(), [[432.5, -432.5], [-432.5, 432.5]])
        self.assertEquals(len(result), 2)
    
    def test_AutoValoresVectores(self):
        matriz_cov = np.matrix([[432.5, -432.5], [-432.5, 432.5]])
        matriz_img = np.matrix([[-9.5, 9.5], [-18.5, 18.5]])
        result_auto_valores, result_auto_vectores = self.foo.DefinirAutoValoresVectores(matriz_cov, matriz_img)
        self.assertEquals(result_auto_valores.tolist(), [865.0])
        self.assertEquals(result_auto_vectores.tolist(), [[-0.4472135954999579], [-0.8944271909999159]])

    def test_Pesos(self):
        matriz_img = np.matrix([[-9.5, 9.5], [-18.5, 18.5]])
        auto_vectores = np.matrix([[-0.4472135954999579], [-0.8944271909999159]])
        result = self.foo.DefinirPesos(matriz_img, auto_vectores)
        self.assertEquals(result.tolist(), [[20.79543219074804, -20.79543219074804]])
        
    def test_Clasificar(self):
        self.foo.CargarImagenes("../Images/")
        self.foo.Entrenar()
        sujeto = self.foo.Clasificar("../Images/s36/6.pgm", self.foo.mean, self.foo.auto_vectores, self.foo.pesos)
        self.foo.listaDeSujetos.GetSujetoAt(sujeto)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()