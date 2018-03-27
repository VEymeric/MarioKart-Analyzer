from PIL import Image
from PIL import ImageChops
from images_functions import *
import cv2

#On stock les pixel x left et x right,y top et y bottom pour les positions des joueurs
#par exemple pour le J1, on est dans le coin haut gauche.
xL = 90
xR = 540
yT = 485
yB = 1000
zJ2 = 160
zJ3  =165
zJ4 = 200
def noname(im2):
    #cv2.imread("../ressources/test/1000.jpg")
    if(abs(im2[xR][yB] - zJ4) < 10):
        return 4
    if(abs(im2[xL][yB] - zJ3) < 10):
        return 3
    if(abs(im2[xR][yT] - zJ2) < 10):
        return 2
    return None


