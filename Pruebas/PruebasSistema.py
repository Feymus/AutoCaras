'''
Created on Nov 12, 2017

@author: DrkSprtn
'''
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait
from selenium.common.exceptions import TimeoutException

class Test(unittest.TestCase):

   
    def setUp(self):
        self.driver = webdriver.Chrome("C:\\selenium-drivers\\chromedriver.exe")

    def test_entrenamiento(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/index.html")
        self.assertIn("ImageRecognition", driver.title)
        vectores = driver.find_element_by_name("quantity1")
        muestras = driver.find_element_by_name("quantity2")
        direccion=driver.find_element_by_name("imagenes")
        entrenar=driver.find_element_by_name("entrenar")
        vectores.send_keys("20")
        muestras.send_keys("30")
        direccion.send_keys("C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images")
        entrenar.click()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
            alert = driver.switch_to_alert()
        except TimeoutException:
            self.fail()
        self.assertEqual("Carga completada!",alert.text )
        alert.accept()
    def test_reconocimiento(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/index.html")
        self.assertIn("ImageRecognition", driver.title)
        vectores = driver.find_element_by_name("quantity1")
        muestras = driver.find_element_by_name("quantity2")
        direccion=driver.find_element_by_name("imagenes")
        entrenar=driver.find_element_by_name("entrenar")
        vectores.send_keys("20")
        muestras.send_keys("30")
        direccion.send_keys("C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images")
        entrenar.click()
        alert=None
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
            alert = driver.switch_to_alert()    
        except TimeoutException:
            self.fail()
        self.assertEqual("Carga completada!",alert.text )
        alert.accept() 
        driver.get("http://127.0.0.1:5000/reconocimiento.html")
        self.assertIn("ImageRecognition", driver.title)
        direccion=driver.find_element_by_name("direccion")
        direccion.send_keys("C:\\Users\\HP\\Desktop\\TEC\\II Semestre 2017\\Aseguramiento de calidad\\Proyecto\\AutoCaras\\Images\\s1"+"\\1.pgm")
        reconocer=driver.find_element_by_name("reconocer")
        reconocer.click()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
            alert = driver.switch_to_alert()    
        except TimeoutException:
            self.fail()
        self.assertEqual("Sujeto identificado como: s1",alert.text )
        alert.accept()
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()