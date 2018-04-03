from images_functions import *
import cv2
import numpy as np
import glob
import os


def find_element_from_database_on_frame(little_frames, database_folder):
    """
    :param frames: multiple images with the same size than databse_folder
    :param database_folder: path to the database of places
    :return: the array of names of element detected and the score
    """
    detected_places = []
    kernel = np.ones((3, 3), np.uint8)

    min_detection_score = len(little_frames)*[50]
    place_detection_result = len(little_frames)*[None]

    database = glob.glob(database_folder + "\*")
    for file in database:
        gradient = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        for i in range(len(little_frames)):
            detected_places.append(cv2.morphologyEx(little_frames[i], cv2.MORPH_GRADIENT, kernel))
            diff = cv2.absdiff(detected_places[i], gradient)
            m_norm = sum(abs(diff))/detected_places[i].size
            if min_detection_score[i] > m_norm:
                min_detection_score[i] = m_norm
                place_detection_result[i] = os.path.basename(file)[:-4]
    return place_detection_result, min_detection_score


def find_laps_on_frame(frame, database_folder, nb_players):
    """
    :param frame: image 1920x1080 already read in grey to scan
    :param database_folder: path to the database of laps
    :param nb_players: integer between 2 and 4
    :return: the array of places and the array of score for these places
    """
    places = []
    # include 2 players here
    if nb_players > 2:
        places.append(frame[475:510,175:195])
        places.append(frame[475:510,1135:1155])
        places.append(frame[1015:1050,175:195])
    if nb_players == 4:
        places.append(frame[1015:1050,1135:1155])

    detected_places = []
    kernel = np.ones((3, 3), np.uint8)

    min_detection_score = nb_players*[50]
    place_detection_resultat = nb_players*[0]

    database = glob.glob(database_folder + "\*")
    for file in database:
        gradient = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        for i in range(nb_players):
            detected_places.append(cv2.morphologyEx(places[i], cv2.MORPH_GRADIENT, kernel))
            diff = cv2.absdiff(detected_places[i], gradient)
            m_norm = sum(abs(diff))/detected_places[i].size
            if min_detection_score[i] > m_norm:
                min_detection_score[i] = m_norm
                place_detection_resultat[i] = os.path.basename(file)[:-4]

    return place_detection_resultat, min_detection_score


def creating_contour_database(init_path, final_path):
    database = glob.glob(init_path + "\*")
    print(database)
    kernel = np.ones((3, 3), np.uint8)
    for file in database:
        new_file = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        new_file = cv2.morphologyEx(new_file, cv2.MORPH_GRADIENT, kernel)
        cv2.imwrite(final_path + name_of_image(file) + ".jpg", new_file)  # save frame as JPEG file


if __name__ == "__main__":
    frame = cv2.cvtColor(cv2.imread("../../testColor/2382.jpg"), cv2.COLOR_BGR2GRAY)
    #frames = [frame[190:280,200:760]]
    frames = [frame[350:580, 410:1500]]
    print(find_element_from_database_on_frame(frames, "../ressources/partez/"))

