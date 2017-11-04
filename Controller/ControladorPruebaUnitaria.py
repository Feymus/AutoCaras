"""
Este modulo gestiona las distintas pruebas unitarias que se han implementado

Created on Aug 19, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
"""
import unittest
from Controller.Controlador import Controlador
import numpy as np
class ControladorTest(unittest.TestCase):
    '''
    Clase ControladorTest
    Clase para el control de pruebas unitarias
    '''
    def setUp(self):
        """
        Esta clase controla lo que tiene que ver con pruebas unitarias de la clase Controlador
        Metodo setUp
        El metodo setUp inicializa todo lo necesario para realizar las pruebas
        """
        self.tester = Controlador()
    def test_cargar_imagenes(self):
        """
        Metodo test_cargar_imagenes
        Prueba del metodo cargar_imagenes en la clase Controlador,
        la prueba se realiza asegurando que se consigan todas las imagenes de los sujetos
        que esten en la direccion dada y confirmando que la lista de sujetos no este vacia y
        que existan imagenes (esto ultimo puede no darse)
        @param url de la carpeta donde se encuentran los sujetos y sus imagenes
        @return Fail si no se cargan las imagenes o los sujetos
        @return Ok si todo cargo correctamente
        """
        result = self.tester.cargar_imagenes("../Images/")
        self.assertEqual(result[0], 0)
        self.assertNotEqual(self.tester.lista_de_sujetos.get_all_imgs(), [])
        self.assertNotEqual(self.tester.lista_de_sujetos.lista_general, [])
    ## Metodo test_vectorizar_imagen
    #
    def test_vectorizar_imagen(self):
        """
        Metodo test_vectorizar_imagen
        Prueba del metodo vectorizar_imagen en la clase Controlador, la prueba
        se realiza asegurando que la imagen se haya aplanado a 1 dimension
        y confirmando el tamano final de la imagen
        @param matrix con listas simulando una imagen
        @return Fail si no se aplano la imagen o si no tiene el tamao adecuado
        @return Ok en caso contrario
        """
        result = self.tester.vectorizar_imagen([[1, 2], [3, 4]])
        lista_resultado = np.array([1, 2, 3, 4], dtype='float64')
        self.assertEqual(result.tolist(), lista_resultado.tolist())
        self.assertEqual(len(result), 4)
    def test_matriz_de_imagenes(self):
        """
        Metodo test_matriz_de_imagenes
        Prueba del metodo definir_matriz_de_imagenes en la case Controlador,
        la prueba se realiza asegurando el resultado de la matriz
        segun una lista de "imagenes"
        @param matrix con listas de "imagenes"
        @return Fail si no se consiguio la matriz de imagenes vectorizadas o si el mean
        es incorrecto
        @return Ok en caso contrario
        """
        imagenes = [[[1, 3]], [[20, 40]]]
        result, mean = self.tester.definir_matriz_de_imagenes(imagenes)
        self.assertEqual(result.tolist(), [[-9.5, 9.5], [-18.5, 18.5]])
        self.assertEqual(mean.tolist(), [10.5, 21.5])
    def test_matriz_de_covarianza(self):
        """
        Metodo test_matriz_de_covarianza
        Prueba del metodo definir_matriz_de_covarianza en la case Controlador,
        la prueba se realiza asegurando el resultado de la matriz
        segun la cantidad de "imagenes"
        @param matrix de "imagenes" vectorizadas
        @return Fail si no es la matriz de covarianza correcta o si tiene el tamano incorrecto
        @return Ok en caso contrario
        """
        result = self.tester.definir_matriz_de_covarianza(np.matrix([[-9.5, 9.5], [-18.5, 18.5]]))
        self.assertEqual(result.tolist(), [[432.5, -432.5], [-432.5, 432.5]])
        self.assertEqual(len(result), 2)
    def test_auto_valores_vectores(self):
        """
        Metodo test_auto_valores_vectores
        Prueba del metodo definir_auto_valores_vectores en la case Controlador,
        la prueba se realiza asegurando que los autovalores y autovectores
        sean los correctos dada una matriz de imagenes vectorizadas y su respectiva
        matriz de covarianza
        @param matrix de covarianza
        @param matrix de "imagenes" vectorizadas
        @return Fail si los auto valores son incorrectos o si los autovectores son incorrectos
        @return Ok en caso contrario
        """
        matriz_cov = np.matrix([[432.5, -432.5], [-432.5, 432.5]])
        matriz_img = np.matrix([[-9.5, 9.5], [-18.5, 18.5]])
        # pylint: disable-msg=C0301
        result_auto_valores, result_auto_vectores = self.tester.definir_auto_valores_vectores(matriz_cov, matriz_img)
        self.assertEqual(result_auto_valores.tolist(), [865.0])
        # pylint: disable-msg=C0301
        self.assertEqual(result_auto_vectores.tolist(), [[-0.4472135954999579], [-0.8944271909999159]])

    def test_pesos(self):
        """
        Metodo test_pesos
        Prueba del metodo definir_pesos en la case Controlador,
        la prueba se realiza asegurando que los pesos
        sean los correctos dada una matriz de imagenes vectorizadas y sus respectivos
        autovectores
        @param auto_vectores
        @param matrix de "imagenes" vectorizadas
        @return Fail si los pesos (imagenes proyectadas) son incorrectas
        @return Ok en caso contrario
        """
        matriz_img = np.matrix([[-9.5, 9.5], [-18.5, 18.5]])
        auto_vectores = np.matrix([[-0.4472135954999579], [-0.8944271909999159]])
        result = self.tester.definir_pesos(matriz_img, auto_vectores)
        self.assertEqual(result.tolist(), [[20.79543219074804, -20.79543219074804]])
    def test_clasificar(self):
        """
        Metodo test_clasificar
        Prueba del metodo clasificar en la case Controlador,
        la prueba se realiza asegurando que la clasificacion
        sea la correcta dada una imagen cuya clasificion es conocida
        autovectores
        @param url de las iamgenes a entrenar
        @param url de la imagen a reconocer
        @return Fail si reconoce incorrectamente al sujeto
        @return Ok en caso contrario
        """
        self.tester.cargar_imagenes("../Images/", _num_para_entrenar=8)
        self.tester.entrenar("prueba_unitaria1", 0.85)
        # pylint: disable-msg=C0301
        id_sujeto = self.tester.clasificar("../Images/s36/8.pgm", "prueba_unitaria1", False)
        sujeto = self.tester.lista_de_sujetos.get_sujeto_at(id_sujeto)
        self.assertEqual(sujeto[1], "s36")
    def test_carga_de_entrenamiento(self):
        """
        Metodo test_carga_de_entrenamiento
        Prueba del metodo cargar_entrenamiento en la case Controlador,
        la prueba se realiza asegurando que el entrenamiento
        se cargue correctamente luego de haberlo guardado en memoria
        @param prefijo del entrenamiento a guardar y cargar
        @return Fail si los auto vectores e imagenes proyectadas no son
        iguales despues y antes de guardar
        @return Ok en caso contrario
        """
        self.tester.cargar_imagenes("../Images/")
        self.tester.entrenar("prueba_unitaria2", 0.85)
        # pylint: disable-msg=C0301
        auto_vectores_actuales = self.tester.auto_vectores
        imagenes_proyectadas_actuales = self.tester.pesos
        self.tester.cargar_entrenamiento("prueba_unitaria2")
        auto_vectores_cargados = self.tester.auto_vectores
        imagenes_proyectadas_cargados = self.tester.pesos
        self.assertEqual(auto_vectores_actuales.tolist(), auto_vectores_cargados.tolist())
        self.assertEqual(imagenes_proyectadas_actuales.tolist(), imagenes_proyectadas_cargados.tolist())
    def test_guardar_entrenamiento(self):
        """
        Metodo test_guardar_entrenamiento
        Prueba del metodo guardar_entrenamiento en la clase Controlador
        La prueba se realiza asegurando que el entrenamiento
        se guarde correctamente
        @param prefijo del entrenamiento para guardar
        @return Fail si no se guardaron correctamente los arreglos
        @return Ok en caso contrario
        """
        self.tester.auto_vectores = np.array([0,0,0])
        self.tester.mean = np.array([0,0,0])
        self.tester.pesos = np.array([0,0,0])
        self.tester.guardar_entrenamiento("prueba_unitaria3")
        nbr_auto_vectores = "prueba_unitaria3_auto_caras.txt"
        self.tester.auto_vectores = np.loadtxt('../datos/entrenamientos/'
                                                   + nbr_auto_vectores, dtype='float64')
        nbr_mean = "prueba_unitaria3_mean.txt"
        self.tester.mean = np.loadtxt('../datos/entrenamientos/' + nbr_mean, dtype='float64')
        nbr_pesos = "prueba_unitaria3_proyecciones.txt"
        self.tester.pesos = np.loadtxt('../datos/entrenamientos/'
                                                 + nbr_pesos, dtype='float64')
        self.assertEqual(self.tester.auto_vectores.tolist(), [0, 0, 0])
        self.assertEqual(self.tester.mean.tolist(), [0, 0, 0])
        self.assertEqual(self.tester.pesos.tolist(), [0, 0, 0])
    def test_get_precision(self):
        """
        Metodo test_get_precision
        Prueba del metodo get_precision en la clase Cotrolador
        La prueba se realiza asegurando que se realice la precision
        correctamente revisando la salida del metodo
        @param prefijo, del entrenamiento a usar
        @return Fail si no se realiza la precision correctamente
        @return Ok  en caso contrario
        """
        self.tester.cargar_imagenes("../Images/")
        self.tester.entrenar("prueba_unitaria4", 0.85)
        self.tester.cargar_entrenamiento("prueba_unitaria4")
        self.tester.url_sujetos = "../Images"
        result = self.tester.get_precision()
        self.assertEqual(result[0], 0)
    def test_agregar_sujeto(self):
        """
        Metodo test_agregar_sujeto
        Prueba del metodo agregar_sujeto en la clase Cotrolador
        La prueba se realiza asegurando que un sujeto se agregue correctamente
        a la lista de sujetos
        @param dict_sujeto, diccionario representando los datos
        pricipales de un sujeto
        @return Fail si no se guarda al sujeto
        @retunr Ok en cualquier otro caso
        """
        dict_sujeto = {}
        dict_sujeto["nombre"] = "sujeto_1"
        dict_sujeto["fotos"] = []
        self.tester.agregar_sujeto(dict_sujeto)
        result = self.tester.lista_de_sujetos.get_sujeto_at(1)
        self.assertEqual(result[1], "sujeto_1")
    def test_carga_inicial(self):
        """
        Metodo test_carga_inicial
        Prueba del metodo cargar_inicial en la case Controlador,
        la prueba se realiza asegurando que el entrenamiento
        se cargue correctamente luego de haberlo guardado en archivos
        @param null
        @return Fail si no se cargan los entrenamientos guardados
        @return Ok en caso contrario
        """
        self.tester.carga_inicial()
        self.assertNotEqual(self.tester.lista_entrenamientos.lista_general, [])
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    