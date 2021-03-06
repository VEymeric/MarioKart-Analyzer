import glob
import os.path
import cv2
import sys
from scipy.misc import imread
from scipy import sum, average
from googlesheet import *
import numpy as np


def name_of_image(path_file):
    return os.path.basename(path_file)[:-4]


def get_grey_images_from_dir(directory):
    files = glob.glob(directory + "\*")
    imgs_grey = []
    for file in files:
        imgs_grey.append(to_grayscale(imread(file).astype(float)))
    return files, imgs_grey


def get_grey_images_from_file(file):
    return to_grayscale(imread(file).astype(float))


def compare_images_value(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    # img1 = normalize(img1)
    # img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    return m_norm/img1.size


def score_compare_image_and_folder(folder, image):
    files, imgs_grey = get_grey_images_from_dir(folder)
    best_index = None
    best_score = 100000000000000
    name_list = []
    score_list = []
    for index, file in enumerate(imgs_grey):
        score = compare_images_value(image, file)
        name_list.append(name_of_image(files[index]))
        score_list.append(score)
        #print(score, name_of_image(files[index]))
        if score < best_score:
            best_score = score
            best_index = index
    return best_score, name_of_image(files[best_index]), name_list, score_list


def is_same_image(img1, img2, score):
    return score > compare_images_value(img1, img2)


def to_grayscale(array):
    """If arr is a color image (3D array), convert it to grayscale (2D array)."""
    if len(array.shape) == 3:
        return average(array, -1)  # average over the last axis (color channels)
    else:
        return array


def normalize(array):
    rng = array.max()-array.min()
    amin = array.min()
    return (array-amin)*255/rng


if __name__ == "__main__":
    image_loading =  cv2.cvtColor(cv2.imread("pop/r.jpg"), cv2.COLOR_BGR2GRAY)[:72]
    image_loading2 =  cv2.cvtColor(cv2.imread("truc.png"), cv2.COLOR_BGR2GRAY)
    image_loading3 =  cv2.cvtColor(cv2.imread("../../testColor/1687.jpg"), cv2.COLOR_BGR2GRAY)[918:990]
    # cv2.imwrite("r.jpg", screen)
    # cv2.imwrite("q.jpg", image_loading)
    # cv2.imwrite("q.jpg", image_loading-screen)
    somme_px_noir1 = np.sum(image_loading == 0)
    somme_px_noir2 = np.sum(image_loading3 == 0)
    print(somme_px_noir1,somme_px_noir2)
