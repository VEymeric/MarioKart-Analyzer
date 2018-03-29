from threading import Thread
from images_functions import *
from detection_functions import *
from Comparaison_Objet_Color import *
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


class CheckState(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""
    def __init__(self, screenshoot):
        Thread.__init__(self)
        self.screenshoot = screenshoot
        self.result = None
    def result(self):
        """Renvoie le résultat lorsqu'il est connu"""
        return self.result
    def run(self):
        self.result = check_state("C:\\Users\ISEN\DocDuC\MK\MarioKart-Analyzer\\ressources\states", self.screenshoot)


class Video(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        MK_video = 'C:\\Users\ISEN\Videos\Capture4.mp4'  # change the file name if needed
        cap = cv2.VideoCapture(MK_video)  # load the video
        count = 0
        loading = "../ressources/miniframe/720.jpg"
        loading = get_grey_images_from_file(loading)
        state = 0
        nb_player = 0
        start_time = time.time()
        while (cap.isOpened()):  # play the video by reading frame by frame
            ret, frame = cap.read()
            if ret == True:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mini_gray = gray_frame[0:100]
                count += 1
                # nb_player = noname(gray_frame)
                if count == 100:
                    supertest = frame[0:200,300:]
                    print(supertest)
                    cv2.imwrite("../ressources/test/" + str(count) + ".jpg", supertest)  # save frame as JPEG file
                if state == 0:  # loading
                    nb_player = selection_persoo(nb_player, frame, gray_frame, count)
                    state = is_loading(state, mini_gray, loading, count)
                elif state == 1:  # end of loading
                    state, last_frame = is_end_of_loading(state, mini_gray, loading, count)
                elif state == 2:  # level name
                    debut = time.time()
                    state = level_name(state, count, last_frame, mini_gray, frame)
                    fin = time.time()
                    print(fin - debut)
                elif state == 3:  # reconnaissance items
                    state = state + 1#run_detection(state,count, last_frame, frame)
                elif state == 4:  # nothing to do, we search the loading for restart
                    state = end_of_run_detection(state)
                #cv2.imwrite("../../testColor/" + str(count) + ".jpg",frame)  # save frame as JPEG file
                if count%200 == 0:
                    print(count, state, nb_player)
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
# Création des threads
thread_3 = Video()

# Lancement des threads
thread_3.start()
