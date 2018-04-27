from threading import Thread
from detection_functions import *  # frame detected
from class_GrandPrix import *
from Changement_De_Place import *
from googlesheet import *
import cv2
import time
from images_functions import *
from Traitement_Objet_Temps_Reel import *
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

LOGS_FILE = '../logs.txt'
DETECTION_ITEM = False

LOADING_SCORE = 7
END_LOADING_SCORE = 10
TEMPO_LEVEL = 30
TEMPO_RUN = 90
LEVEL_SCORE = 10
PARTEZ_SCORE = 35
LAPS_SCORE = 60
PLACES_SCORE = 25
ITEMS_SCORE = 22
TERMINER_SCORE = 22


file_handler = RotatingFileHandler(LOGS_FILE, 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

"""
main class
each Video can detect a GrandPrix
Here are the steps :
0 : search loading - detect nb player
1 : search end of loading
2 : search level
3 : search "partez !"
4 : analyze the race - search the end
5 : search ranking
6 : search GP ranking
7 : analyze the code then restart the step 0
"""


class Video(Thread):
    """Thread de la vidéo."""
    def __init__(self, video):
        Thread.__init__(self)
        self.video = video
        self.loading_file = "../ressources/states/loading.jpg"
        self.partez_file = "../ressources/partez/"
        self.terminer_file = "../ressources/termine/"
        self.objets_foler = "../ressources/objets/used"
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
        reference_statu = 4 * [None]
        compteur_objet = 4 * [0]
        compteur_none = 4 * [0]
        timer_debut_de_course = 0
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
                    if self.gp.state == 1:
                        logger.info("There are %s players on this race", str(self.gp.nb_player))
                elif self.gp.state == 1:  # end of loading
                    if self.gp.nb_player is None:
                        """
                        CAS D'ERREUR CODE EN DURE
                        """
                        self.gp.begin(4)
                        logger.error("Détection nb player failed, init to 4")
                    last_frame = is_end_of_loading(self, loading, END_LOADING_SCORE)
                elif self.gp.state == 2:  # level name
                    name, score = level_name(self, last_frame+TEMPO_LEVEL, LEVEL_SCORE)
                    if name is not None:
                        update(score, 0, 'B', 1)
                elif self.gp.state == 3:  # reconnaissance début de course
                    last_frame = is_partez(self, self.partez_file, PARTEZ_SCORE)
                    if self.gp.state == 4:  # first time we detect the run
                        reference_statu = 4 * [None]
                        compteur_objet = 4 * [0]
                        compteur_none = 4 * [0]
                        timer_debut_de_course = time.time()
                elif self.gp.state == 4 and last_frame+TEMPO_RUN < self.count:  # the race
                    check_places(self, self.positions_folder, PLACES_SCORE)
                    if DETECTION_ITEM:
                        check_items(self, self.objets_foler, ITEMS_SCORE)
                        affiche_objet(self.gp.get_last_run().items_data, reference_statu, compteur_objet, compteur_none)
                    detect_tour(self, self.laps_folder, timer_debut_de_course, LAPS_SCORE)
                    last_frame = is_terminer(self, self.terminer_file, timer_debut_de_course, TERMINER_SCORE)
                elif self.gp.state == 5 and self.count == last_frame:  # we search the ranking
                    calcul_points(self.gp, classement(self.frame, self.count), self.logger)
                    self.gp.state = 6
                elif self.gp.state == 6:
                    if self.gp.final_score_position == [0] * self.gp.nb_player:
                        self.gp.final_score_position = classement(self.frame, self.count)
                        self.gp.state = 7
                    elif grand_prix(self):
                        self.gp.state = 7
                elif self.gp.state == 7:
                    set_positions_on_googlesheet(self.gp.get_last_run().positions_data)
                    self.gp.get_last_run().timers(self.logger)
                    # logger.debug("ITEMS : %s", self.gp.get_last_run().items_data)
                    logger.info("SCORES : %s", self.gp.final_score_points)
                    logger.info("GP classment : %s", self.gp.final_score_position)
                    set_places_on_googlesheet(detection_changement_place(remplissage_tab(
                        self.gp.get_last_run().positions_data)), 2)
                    self.gp.state = 0
                # if self.count % 300 == 0:
                    # for debug only
                    # print("frame : " + str(self.count), "step :" + str(self.gp.state), "players : ", str(self.gp.nb_player))
                    # print("temps d'exécution : ", time.time() - debut)
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


# for read a video
# Video('mypath/MK.mp4').start()
# for read a capture
Video(1).start()
