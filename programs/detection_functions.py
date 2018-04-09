from images_functions import *
from Comparaison_Objet_Color import *
from course_functions import *
from Verification import *
from class_GrandPrix import *

big_array_places = [[], [], [], []]


def is_loading(video, loading_screen, score):
    mini_gray = video.gray_frame[0:100]
    if compare_images_value(mini_gray, loading_screen) < score:
        print(str(video.count) + " : loading :" + str(compare_images_value(mini_gray, loading_screen)))
        video.gp.state += 1


def is_end_of_loading(video, loading_screen, score):
    if compare_images_value(video.gray_frame[:100], loading_screen) > score:
        print(str(video.count) + " : end loading")
        # cv2.imwrite("../ressources/tests/%d.jpg" % count, frame)  # save frame as JPEG file
        video.gp.state += 1
        return video.count
    return 0


def level_name(video, frame_to_check, score_level):
    if video.count == frame_to_check:
        score, name = score_compare_image_and_folder("../ressources/maps/", video.gray_frame[:100], True)
        if score < score_level:
            print(str(name) + " : " + str(score))
            video.gp.run.append(Run(video.gp.nb_player, name))
        video.gp.state += 1


def is_partez(video, partez, scorme_detect):
    frame = video.gray_frame
    frames = [frame[390:550, 425:1330]]
    score, name = score_compare_image_and_folder(partez, frames[0], False)
    if score < scorme_detect:
        print("PARTEZ : ", video.count, score)
        #cv2.imwrite("../ressources/TEST/" + str(video.count) + ".jpg", frame)  # save frame as JPEG file
        video.gp.state += 1


def check_places(video, database_folder):
    frame = video.gray_frame
    little_frames = []
    if video.gp.nb_player > 2:
        little_frames.append(frame[430:500, 830:875])
        little_frames.append(frame[430:500, 1790:1835])
        little_frames.append(frame[970:1040, 830:875])
    if video.gp.nb_player == 4:
        little_frames.append(frame[970:1040, 1790:1835])
    places, score = (video.count, find_element_from_database_on_frame(little_frames, database_folder,25))[1]
    for i in range(video.gp.nb_player):
        video.gp.get_last_run().positions_data[i].append(places[i])
    Verification(video.gp.get_last_run().positions_data, video.gp.nb_player)

def is_terminer(video, terminer, score_detect):
    little_frames = [video.gray_frame[210:280,210:680]]
    """
    if video.nb_player > 2:
        little_frames.append(frame[430:500, 830:875])
        little_frames.append(frame[430:500, 1790:1835])
        little_frames.append(frame[970:1040, 830:875])
    if video.nb_player == 4:
        little_frames.append(frame[970:1040, 1790:1835])
    """
    score, name = score_compare_image_and_folder(terminer, little_frames[0], False)
    if score < score_detect:
        print("TERMINER j1 : ", video.count, score)
        video.gp.state = 5

def run_detection(state, count, last_frame, frame):
    if(count>2580):
        print(count)
        comparaisonObjet(glob.glob("../ressources/Objets/30_30/*"), frame)
    return state

def end_of_run_detection(state):
    return 0


yT= 90
yB = 540
xL = 485
xR = 1000
zJ1 = [ 19,233, 252]
zJ2 = [240, 170, 23]
zJ3 = [138, 131,  240]
zJ4 = [83, 255, 131]


def selection_perso(video):
    nb_player = 0
    #print(video.frame[yT][xL][0], video.frame[yT][xL][1], video.frame[yT][xL][2])
    #print(video.frame[yB][xL][0], video.frame[yB][xL][1], video.frame[yB][xL][2])
    if abs(video.frame[yT][xL][0] - zJ1[0]) < 20 and abs(video.frame[yT][xL][1] - zJ1[1]) < 20 and abs(video.frame[yT][xL][2] - zJ1[2]) < 20:
        if abs(video.frame[yB][xR][0] - zJ4[0]) < 20 and abs(video.frame[yB][xR][1] - zJ4[1]) < 20 and abs(video.frame[yB][xR][2] - zJ4[2]) < 20:
            nb_player = 4
        elif abs(video.frame[yB][xL][0] - zJ3[0]) < 20 and abs(video.frame[yB][xL][1] - zJ3[1]) < 20 and abs(video.frame[yB][xL][2] - zJ3[2]) < 20:
            nb_player = 3
        elif abs(video.frame[yT][xR][0] - zJ2[0]) < 20 and abs(video.frame[yT][xR][1] - zJ2[1]) < 20 and abs(video.frame[yT][xR][2] - zJ2[2]) < 20:
            nb_player = 2
        else:
            nb_player = 1
        video.gp.begin(nb_player)


if __name__ == "__main__":
    screen = cv2.imread("../ressources/states/615.jpg")
    loading = cv2.imread("../ressources/states/loading613.jpg")

    #screen = "../ressources/test/1600.jpg"
    test = screen[0:100]
    print(compare_images_value(loading, test))
    print(compare_images_value(test, loading))
    print(compare_images_value(loading2, test))
    print(compare_images_value(test, loading2))
    print(compare_images_value(loading, loading2))
