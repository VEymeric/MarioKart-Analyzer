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

############################################
# cette partie rempli la liste de fin de course

# plus petite liste
def len_J_Min(list):
    min = list[0]
    a = len(min)
    index = 0
    for i in range(1, len(list)):
        other = list[i]
        b = len(other)
        if(b<a):
            min = list[i]
            a = len(min)
            index = i
    return index

#plus grande liste
def len_J_Max(list):
    max = list[0]
    a = len(max)
    index = 0
    for i in range(1, len(list)):
        other = list[i]
        b = len(other)
        if (b > a):
            max = list[i]
            a = len(max)
            index = i
    return index

# remplissage
def remplissage_tab(list):
    for j in range(0,len(list)):
        min = len_J_Min(list)
        a = list[min]

        max = len_J_Max(list)
        b= list[max]

        for i in range(len(a),len(b)):
            a.append(a[len(a)-1])
            #print(len(a)-1)
    return list

###########################################
# cet partie detect les changements de la nouvelle liste


def detection_changement_place(tableau):
    J1 = tableau[0]
    len_reference = len(J1)
    if (len(tableau)==1):
        tableau_final = [[]]
    if (len(tableau)==2):
        tableau_final= [[],[]]
    if (len(tableau)==3):
        tableau_final = [[],[], []]
    if (len(tableau) == 4):
        tableau_final = [[],[],[],[]]
    place_reference = []
    liste_frame = []
    for k in range(0, len(tableau)):
        J = tableau[k]
        place_reference.append(0)
    for i in range(0,len_reference):
        for j in range(0,len(tableau)):
            J = tableau[j]
            if (J[i]!= place_reference[j] and J[i] is not None):
                for k in range(0, len(tableau)):
                    K = tableau[k]
                    F = tableau_final[k]
                    F.append(K[i])
                    place_reference[k] = K[i]
                liste_frame.append(i)
    return tableau_final, liste_frame
############################