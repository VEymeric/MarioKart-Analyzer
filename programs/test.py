from PIL import Image
from PIL import ImageChops
from images_functions import *
import cv2


im1 = "../ressources/miniframe/secure/Volcant Grondant 61.2728903839.jpg"
f1 = "../ressources/maps"
im2 = "../ressources/miniframe/1740.jpg"

im1 = get_grey_images_from_file(im1)
im2 =  get_grey_images_from_file(im2)
print(score_compare_image_and_folder(f1,  im1))
