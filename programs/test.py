from PIL import Image
from PIL import ImageChops
from images_functions import *
import cv2

#On stock les pixel x left et x right,y top et y bottom pour les positions des joueurs
#par exemple pour le J1, on est dans le coin haut gauche.
frame = cv2.imread("../ressources/test/986.jpg")
yT= 90
yB = 540
xL = 485
xR = 1000
zJ1 = [ 19 ,233, 252]
zJ2 = [240, 170, 23]
zJ3  =[138, 131,  240]
zJ4 = [ 83, 255, 131]
print(frame[yT][xL])
print(frame[yT][xR])
print(frame[yB][xL])
print(frame[yB][xR])
if abs(frame[yB][xL][0] - zJ3[0]) < 5 and abs(frame[yB][xL][1] - zJ3[1]) < 5 and abs(frame[yB][xL][2] - zJ3[2]) < 5:
    print(True)
else:
    print("tt")

if(True):
    if abs(frame[yT][xL][0] - zJ1[0]) < 5 and abs(frame[yT][xL][1] - zJ1[1]) < 5 and abs(frame[yT][xL][2] - zJ1[2]) < 5:
        if abs(frame[yB][xR][0] - zJ4[0]) < 5 and abs(frame[yB][xR][1] - zJ4[1]) < 5 and abs(frame[yB][xR][2] - zJ4[2]) < 5:
            value = 4
        elif abs(frame[yB][xL][0] - zJ3[0]) < 5 and abs(frame[yB][xL][1] - zJ3[1]) < 5 and abs(frame[yB][xL][2] - zJ3[2]) < 5:
            value = 3
        elif abs(frame[yT][xR][0] - zJ2[0]) < 5 and abs(frame[yT][xR][1] - zJ2[1]) < 5 and abs(frame[yT][xR][2] - zJ2[2]) < 5:
            value = 2
        else:
            value = 1
        print(value)

def selection_perso():
    if(abs(frame[xL][yT] - zJ1) < 10):
        test = test
def noname(im2):
    #cv2.imread("../ressources/test/1000.jpg")
    if(abs(im2[xR][yB] - zJ4) < 10):
        return 4
    if(abs(im2[xL][yB] - zJ3) < 10):
        return 3
    if(abs(im2[xR][yT] - zJ2) < 10):
        return 2
    return None


