"""Este modulo gestiona las distintas pruebas unitarias que se han implementado
"""
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
class ControladorTest(unittest.TestCase):
    "# Esta clase controla lo que tiene que ver con pruebas unitarias de la clase Controlador"
    ## Metodo setUp
    #
    # El metodo setUp inicializa todo lo necesario para realizar las pruebas
    def setUp(self):
        self.tester = Controlador()
    ## Metodo test_cargar_imagenes
    #
    def test_cargar_imagenes(self):
        """# Prueba del metodo cargar_imagenes en la clase Controlador,
        #la prueba se realiza asegurando que se consigan todas las imagenes de los sujetos
        # que esten en la direccion dada y confirmando que la lista de sujetos no este vacia y
        #que existan imagenes (esto ultimo puede no darse)"""
        result = self.tester.cargar_imagenes("../Images/")
        self.assertEqual(result[0], 0)
        self.assertNotEqual(self.tester.lista_de_sujetos.get_all_imgs(), [])
        self.assertNotEqual(self.tester.lista_de_sujetos.lista_general, [])
    ## Metodo test_vectorizar_imagen
    #
    def test_vectorizar_imagen(self):
        """# Prueba del metodo vectorizar_imagen en la clase Controlador, la prueba
        se realiza asegurando que la imagen se haya aplanado a 1 dimension
        # y confirmando el tamano final de la imagen"""
        result = self.tester.vectorizar_imagen([[1, 2], [3, 4]])
        lista_resultado = np.array([1, 2, 3, 4], dtype='float64')
        self.assertEqual(result.tolist(), lista_resultado.tolist())
        self.assertEqual(len(result), 4)
    ## Metodo test_matriz_de_imagenes
    #
    def test_matriz_de_imagenes(self):
        """# Prueba del metodo definir_matriz_de_imagenes en la case Controlador,
        la prueba se realiza asegurando el resultado de la matriz
        # segun una lista de "imagenes"""
        imagenes = [[[1, 3]], [[20, 40]]]
        result, mean = self.tester.definir_matriz_de_imagenes(imagenes)
        self.assertEquals(result.tolist(), [[-9.5, 9.5], [-18.5, 18.5]])
        self.assertEquals(mean.tolist(), [10.5, 21.5])
    ## Metodo test_matriz_de_covarianza
    #
    def test_matriz_de_covarianza(self):
        """ # Prueba del metodo definir_matriz_de_covarianza en la case Controlador,
        #la prueba se realiza asegurando el resultado de la matriz
        # segun la cantidad de "imagenes"""
        result = self.tester.definir_matriz_de_covarianza(np.matrix([[-9.5, 9.5], [-18.5, 18.5]]))
        self.assertEquals(result.tolist(), [[432.5, -432.5], [-432.5, 432.5]])
        self.assertEquals(len(result), 2)
    def test_auto_valores_vectores(self):
        """Prueba del metodo AutoValoresVectores en la case Controlador,
        #la prueba se realiza asegurando que los autovalores y autovectores
        #sean los correctos dada una matriz de imagenes vectorizadas y su respectiva
        #matriz de covarianza"""
        matriz_cov = np.matrix([[432.5, -432.5], [-432.5, 432.5]])
        matriz_img = np.matrix([[-9.5, 9.5], [-18.5, 18.5]])
        # pylint: disable-msg=C0301
        result_auto_valores, result_auto_vectores = self.tester.definir_auto_valores_vectores(matriz_cov, matriz_img)
        self.assertEquals(result_auto_valores.tolist(), [865.0])
        # pylint: disable-msg=C0301
        self.assertEquals(result_auto_vectores.tolist(), [[-0.4472135954999579], [-0.8944271909999159]])

    def test_pesos(self):
        """Prueba del metodo Pesos en la case Controlador,
        #la prueba se realiza asegurando que los pesos
        #sean los correctos dada una matriz de imagenes vectorizadas y sus respectivos
        #autovectores"""
        matriz_img = np.matrix([[-9.5, 9.5], [-18.5, 18.5]])
        auto_vectores = np.matrix([[-0.4472135954999579], [-0.8944271909999159]])
        result = self.tester.definir_pesos(matriz_img, auto_vectores)
        self.assertEquals(result.tolist(), [[20.79543219074804, -20.79543219074804]])
    def test_clasificar(self):
        """Prueba del metodo Clasificar en la case Controlador,
        #la prueba se realiza asegurando que la clasificacion
        #sea la correcta dada una imagen cuya clasificion es conocida
        #autovectores"""
        self.tester.cargar_imagenes("../Images/")
        self.tester.entrenar()
        # pylint: disable-msg=C0301
        sujeto = self.tester.clasificar("../Images/s36/6.pgm", self.tester.mean, self.tester.auto_vectores, self.tester.pesos)
        self.tester.lista_de_sujetos.get_sujeto_at(sujeto)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    