from threading import Thread
from images_functions import *
import cv2
import os
import os.path
import glob
import time

import numpy
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
from PIL import Image, ImageChops


class CheckState(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""
    def __init__(self, screenshoot):
        Thread.__init__(self)
        self.screenshoot = screenshoot
        self.result = None
    def result(self):
        """Renvoie le résultat lorsqu'il est connu"""
        return self.result
    def run(self):
        self.result = check_state("C:\\Users\ISEN\DocDuC\MK\MarioKart-Analyzer\\ressources\states", self.screenshoot)


class Video(Thread):
    """Thread chargé simplement d'afficher un mot dans la console."""
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        MK_video = 'D:\Téléchargements\MK (3)(1).mp4'  # change the file name if needed
        cap = cv2.VideoCapture(MK_video)  # load the video
        count = 0
        loading = "../ressources/miniframe/1740.jpg"
        loading = get_grey_images_from_file(loading)
        last_frame = 0
        state = 0
        start_time = time.time()
        while (cap.isOpened()):  # play the video by reading frame by frame
            ret, frame = cap.read()
            if ret == True:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mini_gray = gray_frame[0:100]
                count += 1
                if count==1800:
                    cv2.imwrite("../ressources/miniframe/%d.jpg" % count, mini_gray)  # save frame as JPEG file
                if(state == 0):  #loading
                    if(compare_images_value(mini_gray, loading) < 2):
                        print(str(count) + " : loading :" + str(compare_images_value(mini_gray, loading)))
                        #check if we are in a real loading
                        #cv2.imwrite("../ressources/miniframe/%d.jpg" % count, frame)  # save frame as JPEG file
                        state = 1
                if(state == 1):  #end of loading
                    if(compare_images_value(mini_gray, loading) > 10):
                        #print(str(count) + " : end loading")
                        state = 2
                        last_frame = count
                        #cv2.imwrite("../ressources/tests/%d.jpg" % count, frame)  # save frame as JPEG file
                if(state == 2):  #level name
                    if(count == (last_frame+30)):
                        score, name = score_compare_image_and_folder("../ressources/miniframe/valide",  mini_gray)
                        if(score < 5):
                            print(str(name) + " : " + str(score))
                        else:
                            #i don't know this map so i check his name :
                            print("new map")
                            test = to_grayscale(frame.astype(float))
                            score, name = score_compare_image_and_folder("../ressources/maps", test)
                            print(score, name)
                            cv2.imwrite("../ressources/miniframe/valide/"+name+" "+str(score)+".jpg", mini_gray)  # save frame as JPEG file
                            cv2.imwrite("../ressources/miniframe/secure/"+name+" "+str(score)+".jpg", frame)  # save frame as JPEG file
                        state = 3
                if(state == 3): #nothing to do, we search the loading for restart
                    if (count == (last_frame + 100)):
                        state = 0
                #if(count%600 == 0):
                    #print(str(count) +" : " + str(time.time() - start_time))
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
# Création des threads
thread_3 = Video()

# Lancement des threads
thread_3.start()

