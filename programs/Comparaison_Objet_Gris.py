import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import cv2

################################################
#fonction pour determiner l'objet des joueurs en mode 4 joueurs
# imgs : dossier contenant les images en nuance de gris
# imgC : image a Comparer, elle doit etre en nuance de gris
# files : dossier contenant toutes les images, sert juste à recupere les noms des images
# numeroJ : numero du joueur
def objet4J(imgs,imgC,files,numeroJ):

    if numeroJ == 1 :
        x1,x2,y1,y2=45,110,60,120
    if numeroJ == 2:
        x1, x2, y1, y2 = 45, 110, 1020, 1080
    if numeroJ == 3:
        x1, x2, y1, y2 = 585, 650, 60,120
    if numeroJ == 4 :
        x1, x2, y1, y2 = 585, 650, 1020, 1080

    index = 0
    find = False
    for img in imgs:
        idem =0
        for i in range(x1,x2):
            for j in range(y1,y2):
                # on prend une marge de nuance de 20
                if (imgC[i][j] >= img[i-x1][j-y1] - 20) & (imgC[i][j] <= img[i-x1][j-y1] + 20):
                   idem += 1 # pixel de même nuance de gris

        correspondance = idem / 3900 * 100 # pourcentage de pixels identiques
        #print(os.path.basename(files[index])[:-4]," correspondance ",correspondance,'%') # ecrit le nom des images

        # si on trouve une image correspondante on quitte la boucle
        if correspondance>=55:
            print("l'objet du joueur",numeroJ,"est : "+os.path.basename(files[index])[:-4] )
            find = True
            return True

        index +=1
    #if find == False :
        #print("pas de correspondance pour le joueur",numeroJ)
    return

################################################
#fonction pour determiner l'objet des joueurs en mode 2 joueurs
def objet2J(imgs,imgC,files,numeroJ):
    if numeroJ == 1 :
        x1,x2,y1,y2=60,180,100,190
    if numeroJ == 2:
        x1, x2, y1, y2 = 60,180,1060,1150
    index = 0
    find = False
    for img in imgs:
        idem =0
        for i in range(x1,x2):
            for j in range(y1,y2):
                # on prend une marge de nuance de 20
                if (imgC[i][j] >= img[i-x1][j-y1] - 20) & (imgC[i][j] <= img[i-x1][j-y1] + 20):
                   idem += 1 # pixel de même nuance de gris

        correspondance = idem / 3900 * 100 # pourcentage de pixels identiques
        #print(os.path.basename(files[index])[:-4]," correspondance ",correspondance,'%') # ecrit le nom des images

        # si on trouve une image correspondante on quitte la boucle
        if correspondance>=55:
            print("l'objet du joueur",numeroJ,"est : "+os.path.basename(files[index])[:-4] )
            find = True
            break

        index +=1
    if find == False :
        print("pas de correspondance pour le joueur",numeroJ)
    return

################################################
# comparaison(chemin du dossier contenant les images , image en gris 1920x1080 à comparer aux images du dossier)
def comparaisonObjet(directory_img, imgC):

    files = glob.glob(directory_img + "\*") # dossier contenant toutes les images

    # dimensions des images
    longueur = 60
    largeur = 65
    pixelTotal = largeur * longueur

    #met toutes les images du dossier dans le tableau imgs en gris
    imgs = []
    for file in files:
        imgs.append(to_grayscale(imread(file).astype(float)))

    # compare les images du dossier avec l'image de la vidéo pour les 4 joueurs
    for i in range(1,5):
        if(objet4J(imgs,imgC,files,i)):
            return True

################################################
def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:

        return average(arr, -1)  # average over the last axis (color channels)

    else:
        return arr

################################################
#choisir le chemin du dossier contenant la bdd , l'image en gris à comparer (si l'mage est en couleur utiliser to_grayscale())
#comparaisonObjet('Objets/4joueurs',to_grayscale(cv2.imread('Screen/imageCourse.png')))



