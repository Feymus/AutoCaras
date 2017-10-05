import numpy as np
import cv2
from Model.Sujeto import Sujeto
import random
import os  #libreria para contar la cantidad de fotos por carpeta del sujeto




if __name__ == "__main__":
    #m = np.cov([[1,2],[3,4]])
    #print(m)
    training_ids = random.sample(range(1, 11), 6)
    L = np.empty(shape=(10304, 410))
    img = [1]* 10304
    print("Antes: ", L)
    L[:, 0] = img[:]  
    print("Ahora: ", L)




    