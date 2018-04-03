from images_functions import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
kernel = np.ones((3,3),np.uint8)

debut = time.time()
frame = cv2.imread("../../testColor/3068.jpg")
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
place = []
place.append(gray_frame[430:500, 830:875])
place.append(gray_frame[430:500, 1790:1835])
place.append(gray_frame[970:1040, 830:875])
place.append(gray_frame[970:1040, 1790:1835])

gradientX = []
gradientX.append(cv2.morphologyEx(place[0], cv2.MORPH_GRADIENT, kernel))
gradientX.append(cv2.morphologyEx(place[1], cv2.MORPH_GRADIENT, kernel))
gradientX.append(cv2.morphologyEx(place[2], cv2.MORPH_GRADIENT, kernel))
gradientX.append(cv2.morphologyEx(place[3], cv2.MORPH_GRADIENT, kernel))

mini = [50,50,50,50]
resultat = [0,0,0,0]
files = glob.glob("c/" + "\*")
for file in files:
    gradientY = cv2.imread(file)
    gradientY = cv2.cvtColor(gradientY, cv2.COLOR_BGR2GRAY)
    for i in range(4):
        diff = cv2.absdiff(gradientX[i], gradientY)
        print(diff)
        print(sum(diff))
        m_norm = sum(abs(diff))/gradientX[i].size
        print(os.path.basename(file)[:-4] + " : " + str(m_norm))
        if(mini[i] > m_norm):
            mini[i] = m_norm
            resultat[i] = os.path.basename(file)[:-4]
print(resultat)
print(mini)
print(time.time() - debut)