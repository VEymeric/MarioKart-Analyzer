from threading import Thread
from detection_functions import * # frame detected
from class_GrandPrix import *
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
#from Comparaison_Objet_Color import *
from images_functions import *


class Video(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self, video):
        Thread.__init__(self)
        self.video = video
        self.loading_file = "../ressources/states/loading.jpg"
        self.partez_file = "../ressources/partez/"
        self.objets_foler = "../ressources/Objets/30_30/"
        self.positions_folder = "../ressources/position/4players/"
        self.level_folder = "../ressources/maps/"
        self.test_folder = "../ressources/TEST/"
        self.count = 0
        self.frame = None
        self.gray_frame = None

    def run(self):
        cap = cv2.VideoCapture(self.video)  # load the video
        cap.set(3, 1920)
        cap.set(4, 1080)

        # pretraitement
        loading = get_grey_images_from_file(self.loading_file)[:100]
        gp = GrandPrix()

        state = 0
        nb_player = 0
        last_frame = 0
        # start_time = time.time()
        while cap.isOpened():  # play the video by reading frame by frame
            ret, self.frame = cap.read()
            if ret:  # the video can capture something
                self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.count += 1
                if self.count == 615:
                    cv2.imwrite(str(self.count) + ".jpg", self.frame)  # save frame as JPEG file
                if state == 0:  # loading
                    mini_gray = gray_frame[0:100]
                    nb_player = selection_perso(self, gray_frame, self.count)
                    gp.begin(nb_player)
                    state = is_loading(state, mini_gray, loading, self.count)
                elif state == 1:  # end of loading
                    mini_gray = gray_frame[0:100]
                    state, last_frame = is_end_of_loading(state, mini_gray, loading, self.count)
                elif state == 2:  # level name
                    mini_gray = gray_frame[0:100]
                    state = level_name(state, self.count, last_frame, mini_gray, self.frame)
                elif state == 3:  # reconnaissance course
                    state = is_partez(state, self.frame, self.partez_file, self.count)
                    big_array_places = [[None, None, None, None]]
                elif state == 4:  # course : places uniquement
                    state = check_places(state, self.count, gray_frame, nb_player)
                elif state == 5:  # nothing to do, we search the loading for restart
                    state = end_of_run_detection(state)

                if self.count%200 == 0:
                    print(self.count, state, nb_player)
                # cv2.imwrite("../ressources/testposition/" + str(count) + ".jpg", frame)  # save frame as JPEG file

            else:
                break
        cap.release()
        cv2.destroyAllWindows()


# for read a video
Video('C:\\Users\ISEN\Videos\Mario Kart All Places.mp4').start()
# for read a capture
# Video(1).start()
