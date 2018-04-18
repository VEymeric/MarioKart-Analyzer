from threading import Thread
from detection_functions import *  # frame detected
from class_GrandPrix import *
from Changement_De_Place import *
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
# from Comparaison_Objet_Color import *
from images_functions import *
from Traitement_Objet_Temps_Reel import *
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

LOGS_FILE = '../logs.txt'
LOADING_SCORE = 7
END_LOADING_SCORE = 10
TEMPO_LEVEL = 30
LEVEL_SCORE = 10
PARTEZ_SCORE = 35
LAPS_SCORE = 55
PLACES_SCORE = 25
ITEMS_SCORE = 15
TERMINER_SCORE = 20

file_handler = RotatingFileHandler(LOGS_FILE, 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Video(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self, video):
        Thread.__init__(self)
        self.video = video
        self.loading_file = "../ressources/states/loading.jpg"
        self.partez_file = "../ressources/partez/"
        self.terminer_file = "../ressources/termine/"
        self.objets_foler = "../ressources/objets/"
        self.positions_folder = "../ressources/position/4players/"
        self.level_folder = "../ressources/maps/"
        self.test_folder = "../ressources/TEST/"
        self.laps_folder = "../ressources/laps/"
        self.count = 0
        self.frame = None
        self.gray_frame = None
        self.gp = GrandPrix()
        self.logger = logger

    def run(self):
        cap = cv2.VideoCapture(self.video)  # load the video
        cap.set(3, 1920)
        cap.set(4, 1080)

        # pretraitement
        loading = get_grey_images_from_file(self.loading_file)[:100]
        last_frame = 0

        reference_statu = 4*[None]
        compteur_objet = 4*[0]
        compteur_none = 4*[0]

        # start_time = time.time()
        logger.info("======= New Video =======")
        while cap.isOpened():  # play the video by reading frame by frame
            ret, self.frame = cap.read()
            if ret:  # the video can capture something
                debut = time.time()
                self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.count += 1
                if self.gp.state == 0:  # loading
                    selection_perso(self)
                    is_loading(self, loading, LOADING_SCORE)
                elif self.gp.state == 1:  # end of loading
                    if self.gp.nb_player is None:
                        """
                        CAS D'ERREUR CODE EN DURE
                        """
                        self.gp.begin(4)
                        logger.error("Détection du nombre de joueur fail, init to 4")
                    last_frame = is_end_of_loading(self, loading, END_LOADING_SCORE)
                elif self.gp.state == 2:  # level name
                    name, score = level_name(self, last_frame+TEMPO_LEVEL, LEVEL_SCORE)
                    if name is not None:
                        update(score, 0, 'B', 1)
                elif self.gp.state == 3:  # reconnaissance début de course
                    last_frame = is_partez(self, self.partez_file, PARTEZ_SCORE)
                elif self.gp.state == 4 and last_frame+90 < self.count:  # course
                    check_places(self, self.positions_folder, PLACES_SCORE)
                    # print("check_places :", time.time() - debut)
                    # debut = time.time()
                    # check_items(self, self.objets_foler, ITEMS_SCORE)
                    # print("check_items :", time.time() - debut)
                    # debut = time.time()
                    # affiche_objet(self.gp.get_last_run().items_data, reference_statu, compteur_objet, compteur_none)
                    # print("affiche_objet : ", time.time() - debut)
                    # debut = time.time()
                    detect_tour(self, self.laps_folder, LAPS_SCORE)
                    # print("detect_tour : ", time.time() - debut)
                    # debut = time.time()
                    last_frame = is_terminer(self, self.terminer_file, TERMINER_SCORE)
                elif self.gp.state == 5 and self.count == last_frame:  # we search the classment
                    # self.gp.get_last_run().set_classement_data = calcul_points(self.gp.get_last_run().
                    # set_classement_data, classement(self.frame))
                    self.gp.state = 6
                elif self.gp.state == 6:
                    if self.gp.final_score_position == [0] * self.gp.nb_player:
                        self.gp.final_score_position = classement(self.frame, self.count)
                        self.gp.state = 7
                    elif grand_prix(self):
                        self.gp.state = 7
                        cv2.imwrite(str(self.count) + ".jpg", self.frame)

                elif self.gp.state == 7:
                    set_positions_on_googlesheet(self.gp.get_last_run().positions_data)
                    logger.info("positions : %s", self.gp.get_last_run().positions_data)
                    logger.info("timers : %s", self.gp.get_last_run().timers())

                    logger.info("GP classment : %s", self.gp.final_score_position)
                    set_places_on_googlesheet(detection_changement_place(remplissage_tab(
                        self.gp.get_last_run().positions_data)), 2)
                    self.gp.state = 0
                if self.count % 300 == 0:
                    logger.info("%s, %s, %s", self.count, self.gp.state, self.gp.nb_player)
                    cv2.imwrite("../TEST/" + str(self.count) + ".jpg", self.frame)
                    print("total : ", time.time() - debut)
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


# for read a video
# Video('C:\\Users\ISEN\Videos\MK (4).mp4').start()
# for read a capture
Video(1).start()
