import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import cv2

def objet4J(imgs,imgC,numeroJ):

    if numeroJ == 1 :
        x1, x2, y1, y2 =70, 100, 75, 105
        #x1,x2,y1,y2=45,110,60,120
    if numeroJ == 2:
        x1, x2, y1, y2 =70, 100,1035, 1065
        #x1, x2, y1, y2 = 45, 110, 1020, 1080
    if numeroJ == 3:
        x1, x2, y1, y2 = 610, 640,75,105
        #x1, x2, y1, y2 = 585, 650, 60,120
    if numeroJ == 4 :
        x1, x2, y1, y2 =610, 640,1035, 1065
        #x1, x2, y1, y2 = 585, 650, 1020, 1080

    index = 0 #pour retrouver le nom de l'image
    max = 0
    indexMax = 0
    for img in imgs:
        idem = 0  # nombre de pixel en commun
        img2 = cv2.imread(img)
        for i in range(x1, x2):
            for j in range(y1, y2):
                if ((imgC[i][j][0] <= img2[i - x1][j - y1][0]+10)&(imgC[i][j][0] >= img2[i - x1][j - y1][0]-10)&(imgC[i][j][1] <= img2[i - x1][j - y1][1]+10)&(imgC[i][j][1] >= img2[i - x1][j - y1][1]-20)&(imgC[i][j][2] <= img2[i - x1][j - y1][2]+10)&(imgC[i][j][2] >= img2[i - x1][j - y1][2]-10)):
                    idem += 1
        correspondance = idem / 900 * 100  # pourcentage de pixels identiques
        #print(os.path.basename(imgs[index])[:-4], " correspondance ", correspondance, '%')  # ecrit le nom des images

        #print(os.path.basename(files[index])[:-4])  # ecrit le nom des images

        if (max < correspondance):
            max = correspondance
            indexMax = index
        index += 1

        #print(correspondance)
    if (max < 20 ):
        return None
        #print("pas de correspondance d'objet pour le joueur", numeroJ)
    else :
        return os.path.basename(imgs[indexMax])[:-4]
        #print("l'objet du joueur", numeroJ, "est : " + os.path.basename(imgs[indexMax])[:-4])

def comparaisonObjet(directory_img, imgC):
    objet=[]
    for i in range(1,5):
        objet.append(objet4J(directory_img,imgC,i))
    print(objet)


#comparaisonObjet(glob.glob("../ressources/Objets/30_30/*"),cv2.imread("Screen/4joueurs/color/imageCourse7.png"))



#dossier = glob.glob("Screen/4joueurs/color/*")
#j=0
#for i in dossier :
#    print(os.path.basename(dossier[j])[:-4])
#    comparaisonObjet(glob.glob("Objets/4joueurs/color/30_30/*"),cv2.imread(i))
#    j+=1