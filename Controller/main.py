'''
Created on Aug 12, 2017

@author: Michael
'''

import numpy as np
from PIL import Image
import os
import cv2

# Consigo la direccion donde se encuentra la imagen
scriptDir = os.path.dirname(__file__)
impath = os.path.join(scriptDir, '../Images/unnamed.jpg')


# Matriz de una imagen (la imagen misma)
image = cv2.imread(impath)
# Cambio a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Over the Clouds", image)
cv2.imshow("Over the Clouds - gray", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



arr=cv2.imread(impath,0) # Matriz de una imagen en escala de grises
flat_arr = arr.ravel() # Vectorizacion de una matriz
print(flat_arr)


#img = Image.open(impath).convert('RGB')
#arr = np.array(img)
#flat_arr = arr.ravel()
#print(flat_arr)


if __name__ == '__main__':
    pass