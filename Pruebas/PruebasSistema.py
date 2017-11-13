'''
Esta clase gestiona tanto la ejecucion de Selenium como el manejo de las pruebas de Sistema
Created on Nov 12, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
'''
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
class SystemTest(unittest.TestCase):
    '''
    Clase SystemTest
    Clase para el control de pruebas de sistema
    '''
    def setUp(self):
        '''
        Este metodo recupera el driver de Chrome,
        el cual es necesario para la ejecucion de Selenium
        '''
        self.driver = webdriver.Chrome("C:\\selenium-drivers\\chromedriver.exe")
    def test_entrenamiento(self):
        """
        Metodo test_entrenamiento
        Prueba que la carga de imagenes y entrenamiento funcionen de manera adecuada
        Ingresa como parametros la cantidad de vectores a utilizar y
        la cantidad de muestras a usar en
        el entrenamiento, junto a la direccion en la que se encuentran las imagenes
        Verifica que el mensaje de carga exitosa sea desplegado
        @param url de la carpeta donde se encuentran los sujetos y sus imagenes
        @return Fail si se excede el tiempo de espera de la alerta o la alterta no es la esperada
        @return Ok si el mensaje de carga exitosa fue desplegado
        """
        driver = self.driver
        driver.get("http://127.0.0.1:5000/index.html")
        self.assertIn("ImageRecognition", driver.title)
        vectores = driver.find_element_by_name("quantity1")
        muestras = driver.find_element_by_name("quantity2")
        direccion = driver.find_element_by_name("imagenes")
        entrenar = driver.find_element_by_name("entrenar")
        vectores.send_keys("20")
        muestras.send_keys("30")
        # pylint: disable-msg=C0301
        direccion.send_keys("C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images")
        entrenar.click()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to_alert()
        except TimeoutException:
            self.fail()
        self.assertEqual("Carga completada!", alert.text)
        alert.accept()
    def test_reconocimiento(self):
        '''
        Metodo test_reconocimiento
        Prueba que el reconocimiento de sujetos funcione de manera adecuada
        Ingresa como parametro la direccion donde se encuentra la imagen a identificar
        Verifica que el sujeto estimado sea el esperado para el caso establecido
        @param url de la carpeta donde se encuentra una imagen perteneciente al sujeto 1
        @return Fail si se excede el tiempo de espera de la alerta o el sujeto no es reconocido
        @return Ok si el sujeto es reconocido de manera exitosa
        '''
        driver = self.driver
        driver.get("http://127.0.0.1:5000/index.html")
        self.assertIn("ImageRecognition", driver.title)
        vectores = driver.find_element_by_name("quantity1")
        muestras = driver.find_element_by_name("quantity2")
        direccion = driver.find_element_by_name("imagenes")
        entrenar = driver.find_element_by_name("entrenar")
        vectores.send_keys("20")
        muestras.send_keys("30")
        # pylint: disable-msg=C0301
        direccion.send_keys("C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images")
        entrenar.click()
        alert = None
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to_alert()
        except TimeoutException:
            self.fail()
        self.assertEqual("Carga completada!", alert.text)
        alert.accept()
        driver.get("http://127.0.0.1:5000/reconocimiento.html")
        self.assertIn("ImageRecognition", driver.title)
        direccion = driver.find_element_by_name("direccion")
        # pylint: disable-msg=C0301
        direccion.send_keys("C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images\\s1"+"\\1.pgm")
        reconocer = driver.find_element_by_name("reconocer")
        reconocer.click()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to_alert()
        except TimeoutException:
            self.fail()
        self.assertEqual("Sujeto identificado como: s1", alert.text)
        alert.accept()
    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    