'''
Created on Aug 19, 2017

@author: HP
'''
import unittest
from Controller.Controlador import Controlador


class ControladorTest(unittest.TestCase):


    def setUp(self):
        self.foo = Controlador()


    def tearDown(self):
        pass


    def test_VectorizarImagen(self):
        result = self.foo.VectorizarImagen("../Images/s1/1.pgm")
        self.assertEqual(len(result), 10304)
        self.assertAlmostEquals(result[0], 131)
        self.assertAlmostEquals(result[-1], 25)
        
    def test_MatrizDeImagenes(self):
        result = self.foo.DefinirMatrizDeImagenes(["../Images/s1/1.pgm", "../Images/s1/2.pgm"])
        self.assertEquals(len(result), 10304)
        self.assertEquals(len(result[0]), 2)
    
    def test_MatrizDeCovarianza(self):
        matrizImgVec = self.foo.DefinirMatrizDeImagenes(["../Images/s1/1.pgm", "../Images/s1/2.pgm", "../Images/s1/3.pgm"])
        result = self.foo.DefinirMatrizDeCovarianza(matrizImgVec)
        self.assertEquals(len(result), 10304)
        self.assertEquals(len(result[0]), 10304)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()