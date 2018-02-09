import random
import sys
from threading import Thread
import time
import cv2

MK_video = 'D:\Téléchargements\mariokart\MK (1).mp4'  # change the file name if needed
cap = cv2.VideoCapture(MK_video)  # load the video
count = 0
while (cap.isOpened()):  # play the video by reading frame by frame
            ret, frame = cap.read()
            if ret == True:
                count += 1
                # optional: do some image processing here
                cv2.imshow("Mario Kart", cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
cap.release()
cv2.destroyAllWindows()