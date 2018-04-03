from threading import Thread
from detection_functions import *

import cv2
import os
import os.path
import glob
import time

import numpy
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
from PIL import Image, ImageChops
from Comparaison_Objet_Color import *
from images_functions import *



class Video(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        mk_video = 'C:\\Users\ISEN\Videos\Mario Kart All Places.mp4'  # change the file name if needed
        cap = cv2.VideoCapture(mk_video)  # load the video
        # cap = cv2.VideoCapture(1)  # load the video
        cap.set(3, 1920)
        cap.set(4, 1080)
        count = 0
        loading = "../ressources/miniframe/720.jpg"
        loading = get_grey_images_from_file(loading)
        state = 0
        nb_player = 0
        last_frame = 0
        # start_time = time.time()
        while cap.isOpened():  # play the video by reading frame by frame
            ret, frame = cap.read()
            if ret:  # the video can capture something
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                count += 1
                # nb_player = noname(gray_frame)
                if state == 0:  # loading
                    mini_gray = gray_frame[0:100]
                    nb_player = selection_persoo(nb_player, frame, gray_frame, count)
                    state = is_loading(state, mini_gray, loading, count)
                elif state == 1:  # end of loading
                    mini_gray = gray_frame[0:100]
                    state, last_frame = is_end_of_loading(state, mini_gray, loading, count)
                elif state == 2:  # level name
                    mini_gray = gray_frame[0:100]
                    state = level_name(state, count, last_frame, mini_gray, frame)
                elif state == 3:  # reconnaissance course
                    state = state + 1  # run_detection(state,count, last_frame, frame)
                elif state == 4:  # nothing to do, we search the loading for restart
                    state = end_of_run_detection(state)

                if count%200 == 0:
                    print(count, state, nb_player)
                cv2.imwrite("../ressources/testposition/" + str(count) + ".jpg", frame)  # save frame as JPEG file

            else:
                break
        cap.release()
        cv2.destroyAllWindows()


# Création des threads
thread_3 = Video()

# Lancement des threads
thread_3.start()
