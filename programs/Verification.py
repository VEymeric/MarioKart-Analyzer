import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import cv2
from PIL import Image
import time


# a faire : terminer ce programme. Il doit renvoyer un tableau modifié de celui en entré apres
# avoir remplacer les None par la place précédente de la liste
# faire un etat None
# s'il y a un etat None pour un joueur, on attend que cela change et quand c'est fait on recupere la nouvelle valeur
#et on la remplace dans les anciens tableau

def Before(donnee,J):
    joueur = donnee[J]
    before = joueur[len(joueur)-2]
    if (before==None):
        return 0
    else :
        return 1

def Now(donnee,J):
    joueur = donnee[J]
    now = joueur[len(joueur)-1]
    #print(now[J])
    if (now==None):
        return 0
    else :
        return 1

def MiseAJour(donnee,J,place):
    i = 0
    joueur = donnee[J] # contient la liste des places du joueur J
    avant_Derniere_Place = joueur[len(joueur)-2] # contient l'avant derniere place enregistrée du joueur J qui est None
    while((avant_Derniere_Place == None)&(len(joueur)-(2+i)>=0)):
        copy = joueur[len(joueur)-(2+i)]
        #print(copy)
        copy=place
        joueur[len(joueur)-(2+i)]=copy
        i+=1
        avant_Derniere_Place = joueur[len(joueur)-(2+i)]

    return donnee


def Transition(donnee, J):
    if (Now(donnee, J) > Before(donnee, J)):  # transition None/place
        joueur = donnee[J] # liste contnant l'historique du joueur J
        place = joueur[len(joueur)-1] #derniere place retenue du joueur J
        nv = MiseAJour(donnee, J, place)
        return nv
    else:
        return donnee

def Verification(donnee,i):
    for i in range(0,i):
        resultat = Transition(donnee,i)
    #return resultat


if __name__ == "__main__":
    donnee = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None],[10,12,11,9]]
    print(donnee)
    #resultat = Transition(donnee,1)
    #print(resultat)
    value = Verification(donnee,4)
    print(value)



