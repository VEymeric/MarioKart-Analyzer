from images_functions import *
import cv2
import numpy as np
import glob
import os
from Verification import *


def find_element_from_database_on_frame(little_frames, database_folder, score_min):
    """
    :param little_frames: multiple images with the same size than databse_folder
    :param database_folder: path to the database of places
    :param score_min: score min to detect the element
    :return: the array of names of element detected and the score
    """
    detected_places = []
    kernel = np.ones((3, 3), np.uint8)

    min_detection_score = len(little_frames)*[score_min]
    name_detection_result = len(little_frames)*[None]

    database = glob.glob(database_folder + "\*")
    # print(database)
    for file in database:
        gradient = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        for i in range(len(little_frames)):
            detected_places.append(cv2.morphologyEx(little_frames[i], cv2.MORPH_GRADIENT, kernel))
            diff = cv2.absdiff(detected_places[i], gradient)
            m_norm = sum(abs(diff))/detected_places[i].size
            # print(m_norm)
            if min_detection_score[i] > m_norm:
                min_detection_score[i] = m_norm
                name_detection_result[i] = os.path.basename(file)[:-4]
    return name_detection_result, min_detection_score


def creating_contour_database(init_path, final_path):
    database = glob.glob(init_path + "\*")
    print(database)
    kernel = np.ones((3, 3), np.uint8)
    for file in database:
        new_file = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        new_file = cv2.morphologyEx(new_file, cv2.MORPH_GRADIENT, kernel)
        cv2.imwrite(final_path + name_of_image(file) + ".jpg", new_file)  # save frame as JPEG file


def calcul_points(tableau_final, tab12):
    test = tableau_final
    for i in range(0, 12):
        if tab12[i] == 'J1':
            test[0] += ajoute_point(i)
        if tab12[i] == 'J2':
            test[1] += ajoute_point(i)
        if tab12[i] == 'J3':
            test[2] += ajoute_point(i)
        if tab12[i] == 'J4':
            test[3] += ajoute_point(i)
    return test


def ajoute_point(i):
    if i == 0:
        return 15
    if i == 1:
        return 12
    return 12 - i


def detect_tour(video, database_folder, score_detect):
    little_frames = []
    frame = video.gray_frame
    if video.gp.nb_player > 2:
        little_frames.append(frame[475:505, 170:190])
        little_frames.append(frame[475:505, 1130:1150])
        little_frames.append(frame[1015:1045, 170:190])
    if video.gp.nb_player == 4:
        little_frames.append(frame[1015:1045, 1130:1150])

    for i in range(video.gp.nb_player):
        name, score = (video.count, find_element_from_database_on_frame(little_frames, database_folder, 25))[1]
        if name[i] is not None and int(name[i]) < score_detect:
            if int(name[i]) == len(video.gp.get_last_run().timers_data[i])+1:
                video.gp.get_last_run().timers_data[i].append(video.count)


def check_places(video, database_folder, detection_score):
    frame = video.gray_frame
    little_frames = []
    if video.gp.nb_player > 2:
        little_frames.append(frame[430:500, 830:875])
        little_frames.append(frame[430:500, 1790:1835])
        little_frames.append(frame[970:1040, 830:875])
    if video.gp.nb_player == 4:
        little_frames.append(frame[970:1040, 1790:1835])
    places, score = (video.count, find_element_from_database_on_frame(little_frames, database_folder,
                                                                      detection_score))[1]
    for i in range(video.gp.nb_player):
        if places[i] is None:
            video.gp.get_last_run().positions_data[i].append(None)
        else:
            video.gp.get_last_run().positions_data[i].append(int(places[i]))

    Verification(video.gp.get_last_run().positions_data, video.gp.nb_player)


def check_items(video, database_folder, detection_score):
    frame = video.gray_frame
    little_frames = []
    if video.gp.nb_player > 2:
        little_frames.append(frame[45:110, 60:120])
        little_frames.append(frame[45:110, 1020:1080])
        little_frames.append(frame[585:650, 60:120])
    if video.gp.nb_player == 4:
        little_frames.append(frame[585:650, 1020:1080])
    items, score = (video.count, find_element_from_database_on_frame(little_frames, database_folder,
                                                                     detection_score))[1]
    for i in range(video.gp.nb_player):
        video.gp.get_last_run().items_data[i].append(items[i])