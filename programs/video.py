import numpy as np
import sys
import os
import os.path
import glob
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import cv2


def check_map(arg1, arg2):
    """
    This function compare the full image with the database of maps and return te name of the level
    where the MAnhattan norm is the lowest
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

    # compare
    index = 0
    index_c = 0
    min = 100
    for img in imgs:
        n_m, n_0 = compare_images(image_test, img)
        #print(os.path.basename(files[index_c])[:-4])
        #print("Manhattan norm:", n_m, "/ per pixel:", n_m/img.size)
        #print("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img.size)
        if(n_m/img.size < min):
            index = index_c
            min = n_m/img.size
        index_c += 1
    print("=> ", os.path.basename(files[index])[:-4], " : ", min)

def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

fileName = 'D:\Téléchargements\mariokart\MK (1).mp4'  # change the file name if needed

cap = cv2.VideoCapture(fileName)  # load the video
count = 0
while (cap.isOpened()):  # play the video by reading frame by frame
    ret, frame = cap.read()
    if ret == True:
        count += 1
        # optional: do some image processing here
        cv2.imshow("Mario Kart", cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC))

        if count>2000 and count%60 == 0:
            cv2.imwrite("frame%d.jpg" % ret, frame)  # save frame as JPEG file
            check_map("C:\\Users\ISEN\DocDuC\MK\MarioKart-Analyzer\\ressources\maps", "frame1.jpg")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()