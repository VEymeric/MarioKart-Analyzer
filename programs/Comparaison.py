import cv2
import numpy as np

im1 = cv2.imread('Images/CarapaceVerte2.png')
im2 = cv2.imread('Objets/CarapaceVerte.png')

longueur = 60
largeur = 65
idem =0
pixelTotal = largeur*longueur
for i in range(0,largeur):
    for j in range(0, longueur):
        if (im1[i][j][0] >= im2[i][j][0]-20) & (im1[i][j][1] >= im2[i][j][1]-20) & (im1[i][j][2] >= im2[i][j][2]-20 )&(im1[i][j][0] <= im2[i][j][0]+20) & (im1[i][j][1] <= im2[i][j][1]+20) & (im1[i][j][2] <= im2[i][j][2]+20 ) :
            idem += 1
            print(i,j)

corespondance = idem / pixelTotal *100
print(im2[0][0])
print(im1[0][0])
print(corespondance,' %')