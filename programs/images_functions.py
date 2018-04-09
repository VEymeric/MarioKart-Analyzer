import glob
import os.path
import cv2
import sys
from scipy.misc import imread
from scipy import sum, average
from googlesheet import *


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
    #img1 = normalize(img1)
    #img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    return m_norm/img1.size


def score_compare_image_and_folder(folder, image, update_google_sheet):
    files, imgs_grey = get_grey_images_from_dir(folder)
    best_index = None
    best_score = 100000000000000
    data_google1 = []
    data_google2 = []
    for index, file in enumerate(imgs_grey):
        score = compare_images_value(image, file)
        if client is None:
            update_google_sheet = False
        if(update_google_sheet):
            data_google1.append(name_of_image(files[index]))
            data_google2.append(score)
        #print(score, name_of_image(files[index]))
        if score < best_score:
            best_score = score
            best_index = index
    if (update_google_sheet):
        update(data_google2, 0, 'C' , 1)
    return best_score, name_of_image(files[best_index])


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


def save_image_gray(frame, name, folder):
    #frame = to_grayscale(imread(frame).astype(float))
    cv2.imwrite(folder + "/" + name + ".jpg", frame)  # save frame as JPEG file
