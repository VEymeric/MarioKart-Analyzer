import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import cv2
import time

def place4J(imgs,imgC,numeroJ):

    if numeroJ == 1 :
        x1,x2,y1,y2=430,500,830, 875
    if numeroJ == 2:
        x1, x2, y1, y2 = 430,500,1790,1835
    if numeroJ == 3:
        x1, x2, y1, y2 = 970, 1040,830, 875
    if numeroJ == 4 :
        x1, x2, y1, y2 = 970, 1040,1790, 1835

    index = 0
    find = False

    for img in imgs:
        idem =0
        img2 = cv2.imread(img)

        for i in range(x1,x2):
            for j in range(y1,y2):
                # on prend une marge de nuance de 20
                if (imgC[i][j][0] == img2[i-x1][j-y1][0]):
                   idem += 1 # pixel de même nuance de gris

        correspondance = idem / 3150 * 100 # pourcentage de pixels identiques
        #print(os.path.basename(imgs[index])[:-4]," correspondance ",correspondance,'%') # ecrit le nom des images

        # si on trouve une image correspondante on quitte la boucle
        if correspondance>=55:
            print("la place du joueur",numeroJ,"est : "+os.path.basename(imgs[index])[:-4] )
            find = True
            break

        index +=1
    if find == False :
        #print("pas de correspondance pour le joueur",numeroJ)
        return None
    return os.path.basename(imgs[index])[:-4]

def placePourUnJoueurM(imgC,numeroJ,dossierJ):
    if numeroJ == 1 :
        x1,x2,y1,y2=430,500,830, 875
    if numeroJ == 2:
        x1, x2, y1, y2 = 430,500,1790,1835
    if numeroJ == 3:
        x1, x2, y1, y2 = 970, 1040,830, 875
    if numeroJ == 4 :
        x1, x2, y1, y2 = 970, 1040,1790, 1835
    min = 10000000
    index = 0
    indexMax = 0
    for img in dossierJ:

        nom = os.path.basename(dossierJ[index])[:-7]
        img2 = cv2.imread(img)
        im1=imgC[x1:x2,y1:y2]
        diff = im1 - img2
        m_norm = sum(abs(diff))

        #print(m_norm)
        #print(os.path.basename(dossierJ[index])[:-7], m_norm)
        if (m_norm<min):
            min = m_norm
            indexMax = os.path.basename(dossierJ[index])[:-7]
        index += 1

    #if (min > 100000 ):
         #print("pas de correspondance d'objet pour le joueur", numeroJ)
         #return None

    #else :
    #print("l'objet du joueur", numeroJ, "est : " + os.path.basename(imgs[indexMax])[:-4])
    return indexMax

def boucle4joueurs(imgC):
    objet=[]
    for i in range(1,5):
        #print("Joueur ",i)
        numero = str(i)
        directory_img_Place = glob.glob("../ressources/position/joueur"+numero+"/*")
        objet.append(placePourUnJoueurM(imgC,i,directory_img_Place))

    print(objet)

def main():
    boucle4joueurs(cv2.imread("../ressources/testlive/5800.jpg"))
#placePourUnJoueurM(cv2.imread("Screen/4joueurs/gray/imageCourse7.png"),4,glob.glob("placesJoueurs/4joueurs/gray/Joueur3/*"))
#boucle4joueurs(cv2.imread("Screen/4joueurs/gray/imageCourse6.png"))
debut = time.time()
main()
print(time.time() - debut)