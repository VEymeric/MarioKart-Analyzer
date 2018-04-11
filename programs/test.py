from cv2 import *

image = cv2.imread("../ressources/states/615.jpg")[918:990]
cv2.imwrite("truc.png", image)