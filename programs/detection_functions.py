from images_functions import *
from Comparaison_Objet_Color import *
from course_functions import *
from Verification import *

big_array_places = [[], [], [], []]


def is_loading(state, mini_gray, loading_screen, count):
    if compare_images_value(mini_gray, loading_screen) < 4:
        print(str(count) + " : loading :" + str(compare_images_value(mini_gray, loading_screen)))
        # check if we are in a real loading
        # cv2.imwrite("../ressources/miniframe/%d.jpg" % count, frame)  # save frame as JPEG file
        return state + 1
    # print(compare_images_value(mini_gray, loading_screen))
    return state


def is_end_of_loading(state, mini_gray, loading_screen, count):
    if compare_images_value(mini_gray, loading_screen) > 10:
        print(str(count) + " : end loading")
        # cv2.imwrite("../ressources/tests/%d.jpg" % count, frame)  # save frame as JPEG file
        return state + 1, count
    return state, 0


def level_name(state, count, last_frame, mini_gray, frame):
    if count == (last_frame + 30):
        print("YOLO")
        score, name = score_compare_image_and_folder("../ressources/maps/", mini_gray, [True, ])
        if score < 10:
            print(str(name) + " : " + str(score))
        else:
            # i don't know this map so i check his name :
            print("new map")
            print(str(name) + " : " + str(score))
            cv2.imwrite("../ressources/miniframe/valide/" + name + " " + str(score) + ".jpg",
                        mini_gray)  # save frame as JPEG file
            cv2.imwrite("../ressources/miniframe/secure/" + name + " " + str(score) + ".jpg",
                        frame)  # save frame as JPEG file
        return state + 1
    return state


def is_partez(state, frame, partez, count):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames = [frame[390:550, 425:1330]]
    score, name = score_compare_image_and_folder(partez, frames[0], False)
    if score<25 :
        print("PARTEZ : " ,count, score)
        cv2.imwrite("../ressources/TEST/" + str(count) + ".jpg", frame)  # save frame as JPEG file
        return state + 1
    else:
        return state


def check_places(state, count, frame, nb_player):
    database_folder = "../ressources/position/4players/"
    little_frames = []
    if nb_player > 2:
        little_frames.append(frame[430:500, 830:875])
        little_frames.append(frame[430:500, 1790:1835])
        little_frames.append(frame[970:1040, 830:875])
    if nb_player == 4:
        little_frames.append(frame[970:1040, 1790:1835])
    places, score = (count, find_element_from_database_on_frame(little_frames, database_folder,25))[1]
    for i in range(nb_player):
        big_array_places[i].append(places[i])
    #print(big_array_places)
    Verification(big_array_places, nb_player)

    return state


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


def selection_perso(video, frame, gray_frame, count):
    
    if abs(frame[yT][xL][0] - zJ1[0]) < 5 and abs(frame[yT][xL][1] - zJ1[1]) < 5 and abs(frame[yT][xL][2] - zJ1[2]) < 5:
        if abs(frame[yB][xR][0] - zJ4[0]) < 10 and abs(frame[yB][xR][1] - zJ4[1]) < 5 and abs(frame[yB][xR][2] - zJ4[2]) < 10:
            value = 4
        elif abs(frame[yB][xL][0] - zJ3[0]) < 10 and abs(frame[yB][xL][1] - zJ3[1]) < 5 and abs(frame[yB][xL][2] - zJ3[2]) < 10:
            value = 3
        elif abs(frame[yT][xR][0] - zJ2[0]) < 10 and abs(frame[yT][xR][1] - zJ2[1]) < 5 and abs(frame[yT][xR][2] - zJ2[2]) < 10:
            value = 2
        else:
            value = 1
        return value
    return nb_player


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
