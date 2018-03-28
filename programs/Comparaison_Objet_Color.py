import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import cv2

yezgrzurzer = 12222


def objet4J(imgs,imgC,numeroJ):
    if numeroJ == 1 :
        x1,x2,y1,y2=45,110,60,120
    if numeroJ == 2:
        x1, x2, y1, y2 = 45, 110, 1020, 1080
    if numeroJ == 3:
        x1, x2, y1, y2 = 585, 650, 60,120
    if numeroJ == 4 :
        x1, x2, y1, y2 = 585, 650, 1020, 1080

    index = 0 #pour retrouver le nom de l'image
    max = 0
    indexMax = 0
    for img in imgs:
        idem = 0  # nombre de pixel en commun
        img2 = cv2.imread(img)
        for i in range(x1, x2):
            for j in range(y1, y2):
                if ((imgC[i][j][0] <= img2[i - x1][j - y1][0]+10)&(imgC[i][j][0] >= img2[i - x1][j - y1][0]-10)&(imgC[i][j][1] <= img2[i - x1][j - y1][1]+10)&(imgC[i][j][1] >= img2[i - x1][j - y1][1]-10)&(imgC[i][j][2] <= img2[i - x1][j - y1][2]+10)&(imgC[i][j][2] >= img2[i - x1][j - y1][2]-10)):
                    idem += 1
        correspondance = idem / 3900 * 100  # pourcentage de pixels identiques
        #print(os.path.basename(imgs[index])[:-4], " correspondance ", correspondance, '%')  # ecrit le nom des images

        #print(os.path.basename(files[index])[:-4])  # ecrit le nom des images

        if (max < correspondance):
            max = correspondance
            indexMax = index
        index += 1

        #print(correspondance)
    if (max < 10 ):
        print("pas de correspondance d'objet pour le joueur", numeroJ)
    else :
        print("l'objet du joueur", numeroJ, "est : " + os.path.basename(imgs[indexMax])[:-4])
    return


def comparaisonObjet(directory_img, imgC):
    directory_img = glob.glob(directory_img)
    for i in range(1,5):
        objet4J(directory_img,imgC,i)
    return 1
#comparaisonObjet(glob.glob("Objets/4joueurs/color/*"),cv2.imread("Screen/4joueurs/imageCourse2.png"))


if __name__ == "__main__":
    dossier = glob.glob("Screen/4joueurs"+"\*")
    j=0
    for i in dossier :
        print("Image",j)
        comparaisonObjet(glob.glob("Objets/4joueurs/color/*"),cv2.imread(i))
        j+=1