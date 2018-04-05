from images_functions import *
import cv2
import numpy as np
import glob
import os


def find_element_from_database_on_frame(little_frames, database_folder, score_min):
    """
    :param frames: multiple images with the same size than databse_folder
    :param database_folder: path to the database of places
    :return: the array of names of element detected and the score
    """
    detected_places = []
    kernel = np.ones((3, 3), np.uint8)

    min_detection_score = len(little_frames)*[score_min]
    place_detection_result = len(little_frames)*[None]

    database = glob.glob(database_folder + "\*")
    #print(database)
    for file in database:
        gradient = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        for i in range(len(little_frames)):
            detected_places.append(cv2.morphologyEx(little_frames[i], cv2.MORPH_GRADIENT, kernel))
            diff = cv2.absdiff(detected_places[i], gradient)
            m_norm = sum(abs(diff))/detected_places[i].size
            #print(m_norm)
            if min_detection_score[i] > m_norm:
                min_detection_score[i] = m_norm
                place_detection_result[i] = int(os.path.basename(file)[:-4])
    return place_detection_result, min_detection_score


def creating_contour_database(init_path, final_path):
    database = glob.glob(init_path + "\*")
    print(database)
    kernel = np.ones((3, 3), np.uint8)
    for file in database:
        new_file = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        new_file = cv2.morphologyEx(new_file, cv2.MORPH_GRADIENT, kernel)
        cv2.imwrite(final_path + name_of_image(file) + ".jpg", new_file)  # save frame as JPEG file


"""
if __name__ == "__main__":
    frame = cv2.cvtColor(cv2.imread("../test_unitaire/position/1469.jpg"), cv2.COLOR_BGR2GRAY)
    frames = [frame[430:500,830:875]]
    cv2.imwrite("1.jpg", frames[0])  # save frame as JPEG file

    #frames = [frame[350:580, 410:1500]]
    print(find_element_from_database_on_frame(frames, "../ressources/position/4players/"), 50)
"""
