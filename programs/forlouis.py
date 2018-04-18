from cv2 import *

cap = cv2.VideoCapture('C:\\Users\ISEN\Videos\MK (3).mp4')  # load the video
count = 0
while cap.isOpened():  # play the video by reading frame by frame
    ret, frame = cap.read()
    if ret:  # the video can capture something
        count += 1

    if grand_prix(frame):
        cv2.imwrite("@mettre un dossier ici déjà créé genre /mytest/" + str(count) + ".jpg", frame)