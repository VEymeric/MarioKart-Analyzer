import cv2
im = cv2.imread('imageCourse.png')

################OBJETS################
#objet en haut à gauche
for i in range(45,110):
   for j in range(60,120):
        im[i][j] = [0, 255, 255]

#objet en haut à driote
for i in range(45, 110):
    for j in range(1020, 1080):
        im[i][j] = [0, 255, 255]

#objet en bas à droite
for i in range(585, 650):
    for j in range(1020, 1080):
         im[i][j] = [0, 255, 255]

#objet en bas à gauche
for i in range(585, 650):
     for j in range(60,120):
         im[i][j] = [0, 255, 255]

################PLACES################
#place en haut à droite
for i in range(430, 520):
     for j in range(1776,1860):
         im[i][j] = [0, 255, 255]

# place en haut à gauche
for i in range(430, 520):
    for j in range(816, 900):
        im[i][j] = [0, 255, 255]

# place en bas à droite
for i in range(970, 1060):
    for j in range(1776, 1860):
        im[i][j] = [0, 255, 255]

# place en bas à gauche
for i in range(970, 1060):
    for j in range(816, 900):
        im[i][j] = [0, 255, 255]

################PIECES################
#piece en haut à gauche
for i in range(475,510):
   for j in range(90,130):
        im[i][j] = [0, 255, 255]

#piece en haut à driote
for i in range(475, 510):
    for j in range(1050, 1090):
        im[i][j] = [0, 255, 255]

#piece en bas à droite
for i in range(1015, 1050):
    for j in range(1050, 1090):
         im[i][j] = [0, 255, 255]

#piece en bas à gauche
for i in range(1015, 1050):
     for j in range(90,130):
         im[i][j] = [0, 255, 255]


################TOURS################
# tour en haut à gauche
for i in range(475, 510):
    for j in range(175, 195):
        im[i][j] = [0, 255, 255]

# tour en haut à driote
for i in range(475, 510):
    for j in range(1135,1155 ):
        im[i][j] = [0, 255, 255]

# tour en bas à droite
for i in range(1015,1050 ):
    for j in range(1135,1155):
        im[i][j] = [0, 255, 255]

# tour en bas à gauche
for i in range(1015, 1050):
    for j in range(175, 195):
        im[i][j] = [0, 255, 255]


# sauvegarde du resultat
cv2.imwrite('resultat.png',im)
#print(im)