from threading import Thread
from detection_functions import * # frame detected
from class_GrandPrix import *
from googlesheet import *
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

LOADING_SCORE = 7
END_LOADING_SCORE = 10
TEMPO_LEVEL = 30
LEVEL_SCORE = 10
PARTEZ_SCORE = 25

class Video(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self, video):
        Thread.__init__(self)
        self.video = video
        self.loading_file = "../ressources/states/loading.jpg"
        self.partez_file = "../ressources/partez/"
        self.terminer_file = "../ressources/termine/"
        self.objets_foler = "../ressources/Objets/30_30/"
        self.positions_folder = "../ressources/position/4players/"
        self.level_folder = "../ressources/maps/"
        self.test_folder = "../ressources/TEST/"
        self.count = 0
        self.frame = None
        self.gray_frame = None
        self.gp = GrandPrix()

    def run(self):
        cap = cv2.VideoCapture(self.video)  # load the video
        cap.set(3, 1920)
        cap.set(4, 1080)

        # pretraitement
        loading = get_grey_images_from_file(self.loading_file)[:100]

        state = 0
        nb_player = 0
        last_frame = 0
        # start_time = time.time()
        while cap.isOpened():  # play the video by reading frame by frame
            ret, self.frame = cap.read()
            if ret:  # the video can capture something
                self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.count += 1
                if self.gp.state == 0:  # loading
                    selection_perso(self)
                    is_loading(self, loading, LOADING_SCORE)
                    #self.gp.begin(4)
                elif self.gp.state == 1:  # end of loading
                    last_frame = is_end_of_loading(self, loading, END_LOADING_SCORE)
                elif self.gp.state == 2:  # level name
                    level_name(self, last_frame+TEMPO_LEVEL, LEVEL_SCORE)
                elif self.gp.state == 3:  # reconnaissance course
                    is_partez(self, self.partez_file, PARTEZ_SCORE)
                    big_array_places = [[None, None, None, None]]
                elif self.gp.state == 4:  # course : places uniquement
                    check_places(self, self.positions_folder)
                    is_terminer(self, self.terminer_file, PARTEZ_SCORE)
                elif self.gp.state == 5:  # nothing to do, we search the loading for restart
                    set_positions_on_googlesheet(self.gp.get_last_run().positions_data)
                    self.gp.state = 0
                if self.count%200 == 0:
                    print(self.count, self.gp.state, self.gp.nb_player)
                if self.count % 501 == 0:
                    cv2.imwrite("../ressources/testreel/" + str(self.count) + ".jpg", self.frame)  # save frame as JPEG file

            else:
                break
        cap.release()
        cv2.destroyAllWindows()


# for read a video
Video('C:\\Users\ISEN\Videos\Mario Kart All Places.mp4').start()
# for read a capture
# Video(1).start()
