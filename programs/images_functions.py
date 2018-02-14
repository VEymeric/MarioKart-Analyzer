import glob
import os.path
from scipy.misc import imread
from scipy import sum, average


def name_of_image(path_file):
    return os.path.basename(path_file)[:-4]


def get_grey_images_from_dir(directory):
    files = glob.glob(directory + "\*")
    imgs_grey = []
    for file in files:
        imgs_grey.append(to_grayscale(imread(file).astype(float)))
    return imgs_grey


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
    return m_norm


def is_same_image(img1, img2, score):
    return score <= compare_images_value(img1, img2)


def to_grayscale(array):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(array.shape) == 3:
        return average(array, -1)  # average over the last axis (color channels)
    else:
        return array


def normalize(array):
    rng = array.max()-array.min()
    amin = array.min()
    return (array-amin)*255/rng