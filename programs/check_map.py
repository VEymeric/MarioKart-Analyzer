import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average


def get_grey_images_from_dir(directory):
    files = glob.glob(directory + "\*")
    imgs_grey = []
    for file in files:
        imgs_grey.append(to_grayscale(imread(file).astype(float)))
    return imgs_grey


def get_grey_images_from_file(file):
    return to_grayscale(imread(file).astype(float))



def check_map(arg1, arg2):
    """
    This function compare the full image with the database of maps and return te name of the level
    where the Manhattan norm is the lowest
    2 arguments :
        The path to the directory with all your maps screen
        The image you wanna check
    """
    directory_map = arg1
    image_test = arg2
    image_test = to_grayscale(imread(image_test).astype(float))
    files = glob.glob(directory_map +"\*")
    # read images as 2D arrays (convert to grayscale for simplicity)
    imgs = []
    for file in files:
        imgs.append(to_grayscale(imread(file).astype(float)))
    print(imgs)

    # compare
    index = 0
    index_c = 0
    min = 100
    for img in imgs:
        n_m, n_0 = compare_images(image_test, img)
        print(os.path.basename(files[index_c])[:-4])
        print("Manhattan norm:", n_m, "/ per pixel:", n_m/img.size)
        print("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img.size)
        if(n_m/img.size < min):
            index = index_c
            min = n_m/img.size
        index_c += 1
    print("=> ", os.path.basename(files[index])[:-4])


def check_state(directory_state, image_test):
    """
    This function compare the full image with the database of state and return the name of the stat
    where the Manhattan norm if he is < 15.
    2 arguments :
        The path to the directory with all your state screen
        The image you wanna check
    """
    image_test = to_grayscale(imread(image_test).astype(float))
    files = glob.glob(directory_state +"\*")
    # read images as 2D arrays (convert to grayscale for simplicity)
    imgs = []
    for file in files:
        imgs.append(to_grayscale(imread(file).astype(float)))

    # compare
    index = 0
    index_c = 0
    min = 100
    for img in imgs:
        n_m, n_0 = compare_images(image_test, img)
        print(os.path.basename(files[index_c])[:-4])
        print("Manhattan norm:", n_m, "/ per pixel:", n_m/img.size)
        if(n_m/img.size < min):
            index = index_c
            min = n_m/img.size
        index_c += 1
    print("=> ", os.path.basename(files[index])[:-4], " : ", min)
    if(min <15):
        return os.path.basename(files[index])[:-4]
    return ""


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


if __name__ == "__main__":
    check_map(sys.argv[1],sys.argv[2])