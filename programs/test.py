from images_functions import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
kernel = np.ones((3,3),np.uint8)

debut = time.time()
frame = "../ressources/testposition/3573.jpg"
frame = cv2.cvtColor(cv2.imread(frame), cv2.COLOR_BGR2GRAY)

frame = frame[475:510,175:195]
kernel = np.ones((3, 3), np.uint8)
frame= cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
cv2.imwrite("7.jpg", frame)  # save frame as JPEG file

