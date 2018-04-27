from images_functions import *
from course_functions import *
from class_GrandPrix import *
import cv2
import time


def is_loading(video, loading_screen, score):
    mini_gray = video.gray_frame[0:100]
    black_zone = video.frame[918:990]
    if compare_images_value(mini_gray, loading_screen) < score and np.sum(black_zone == 0) > 1000:
        video.logger.info("%s : loading : %s", str(video.count), str(compare_images_value(mini_gray, loading_screen)))
        video.gp.state += 1
        # cv2.imwrite("../ressources/TEST/" + str(video.count) + "_loading.jpg", video.frame)  # save frame as JPEG file


def is_end_of_loading(video, loading_screen, score):
    if compare_images_value(video.gray_frame[:100], loading_screen) > score:
        video.logger.info("%s : end loading", str(video.count))
        # cv2.imwrite("../ressources/tests/%d.jpg" % count, frame)  # save frame as JPEG file
        video.gp.state += 1
        # cv2.imwrite("../ressources/TEST/" + str(video.count) + "_endloading.jpg", video.frame)  # save frame as JPEG file

        return video.count
    return 0


def level_name(video, frame_to_check, score_level):
    if video.count == frame_to_check:
        score, name, list_score, list_name = score_compare_image_and_folder("../ressources/maps/",
                                                                            video.gray_frame[:100])
        if score < score_level:
            video.logger.info("%s : %s", str(name), str(score))
            video.gp.run.append(Run(video.gp.nb_player, name, video.count))
            video.gp.state += 1
            return list_score, list_name
        cv2.imwrite(str(video.count) + "_level.jpg", video.frame)  # save frame as JPEG file
        video.gp.state += 1
        video.gp.run.append(Run(video.gp.nb_player, None, video.count))

    return None, None


def is_partez(video, partez, scorme_detect):
    frame = video.gray_frame
    frames = frame[390:550, 425:1330]
    score, name, list_score, list_name = score_compare_image_and_folder(partez, frames)
    if score < scorme_detect:
        video.logger.info("PARTEZ : %s %s", video.count, score)
        # cv2.imwrite("../ressources/TEST/" + str(video.count) + "_partez.jpg", video.frame)  # save frame as JPEG file
        video.gp.state += 1
    return video.count


def is_terminer(video, terminer, timer_debut_de_course, score_detect):
    little_frames = []
    frame = video.gray_frame
    if video.gp.nb_player > 2:
        little_frames.append(frame[210:280, 210:680])
        little_frames.append(frame[210:280, 1170:1640])
        little_frames.append(frame[750:820, 210:680])
    if video.gp.nb_player == 4:
        little_frames.append(frame[750:820, 1170:1640])
    for i in range(video.gp.nb_player):
        if video.gp.get_last_run().players_statut_data[i] == 1:
            score, name, list_score, list_name = score_compare_image_and_folder(terminer, little_frames[i])
            if score < score_detect:
                video.logger.info("TERMINER j%s %s : %s", i + 1, video.count, score)
                video.gp.get_last_run().players_statut_data[i] = 0
                video.gp.get_last_run().timers_data[i].append(time.time() - timer_debut_de_course)

                # cv2.imwrite("../ressources/TEST/" + str(video.count) + "_terminer.jpg", video.frame)  # save frame as JPEG file

    if sum(video.gp.get_last_run().players_statut_data) == 0:
        video.gp.state = 5
        return video.count + 100
    return 0


def end_of_run_detection(state):
    return 0


def selection_perso(video):
    nb_player = 0
    yT = 90
    y_seccure_2 = 414
    x_secure_2 = 950
    yB = 540
    xL = 485
    xR = 1000
    zJ1 = [19, 233, 252]
    zJ1_2 = [0, 205, 245]
    zJ2 = [240, 170, 23]
    zJ3 = [138, 131, 240]
    zJ4 = [83, 255, 131]
    # print(video.frame[yT][xL][0], video.frame[yT][xL][1], video.frame[yT][xL][2])
    # print(video.frame[yB][xL][0], video.frame[yB][xL][1], video.frame[yB][xL][2])
    if (abs(video.frame[yT][xL][0] - zJ1[0]) < 20 and abs(video.frame[yT][xL][1] - zJ1[1]) < 20 and abs(
                video.frame[yT][xL][2] - zJ1[2]) < 20) and \
            (abs(video.frame[y_seccure_2][x_secure_2][0] - zJ1_2[0]) < 20 and abs(
                    video.frame[y_seccure_2][x_secure_2][1] - zJ1_2[1]) < 20 and abs(
                    video.frame[y_seccure_2][x_secure_2][2] - zJ1_2[2]) < 20):
        cv2.imwrite("../TESTI/" + str(video.count) + ".jpg", video.frame)
        if abs(video.frame[yB][xR][0] - zJ4[0]) < 20 and abs(video.frame[yB][xR][1] - zJ4[1]) < 20 and abs(
                        video.frame[yB][xR][2] - zJ4[2]) < 20:
            nb_player = 4
        elif abs(video.frame[yB][xL][0] - zJ3[0]) < 20 and abs(video.frame[yB][xL][1] - zJ3[1]) < 20 and abs(
                        video.frame[yB][xL][2] - zJ3[2]) < 20:
            nb_player = 3
        elif abs(video.frame[yT][xR][0] - zJ2[0]) < 20 and abs(video.frame[yT][xR][1] - zJ2[1]) < 20 and abs(
                        video.frame[yT][xR][2] - zJ2[2]) < 20:
            nb_player = 2
        else:
            nb_player = 1
        video.gp.begin(nb_player)


# 239 // 242 // 41
def classement(frame, count):
    x = 960
    y = [80, 160, 240, 320, 400, 470, 550, 630, 710, 780, 860, 940]
    zJ1 = [50, 222, 238]  # Jaune
    zJ2 = [240, 230, 85]  # Bleu
    zJ3 = [140, 135, 237]  # Rouge
    zJ4 = [75, 247, 135]  # Vert
    tabfinal = ['IA'] * 12
    for j, i in enumerate(y):
        (bleu, vert, rouge) = frame[i, x]
        if abs(bleu - zJ1[0]) < 55 and abs(vert - zJ1[1]) < 30 and abs(rouge - zJ1[2]) < 30:
            # print "Joueur Jaune"
            tabfinal[j] = 'J1'
        elif abs(bleu - zJ2[0]) < 30 and abs(vert - zJ2[1]) < 30 and abs(rouge - zJ2[2]) < 30:
            # print "Joueur Bleu"
            tabfinal[j] = 'J2'
        elif abs(bleu - zJ3[0]) < 30 and abs(vert - zJ3[1]) < 30 and abs(rouge - zJ3[2]) < 30:
            # print "Joueur Rouge"
            tabfinal[j] = 'J3'
        elif abs(bleu - zJ4[0]) < 55 and abs(vert - zJ4[1]) < 30 and abs(rouge - zJ4[2]) < 30:
            # print "Joueur Vert"
            tabfinal[j] = 'J4'
    return tabfinal


def grand_prix(video):
    x1 = 490
    y1 = 110
    y2 = 970
    kJ1 = [16, 185, 40]  # Vert
    kJ2 = [15, 114, 243]  # Orange
    kJ3 = [247, 123, 0]  # Bleu
    (bleu, vert, rouge) = video.frame[y1, x1]
    # print (bleu, vert, rouge)
    (blue, green, red) = video.frame[y2, x1]
    # print (blue, green, red)

    if ((abs(bleu - kJ1[0]) < 10 and abs(vert - kJ1[1]) < 30
         and abs(rouge - kJ1[2]) < 10) or (abs(bleu - kJ2[0]) < 10
                                           and abs(vert - kJ2[1]) < 20 and abs(rouge - kJ2[2]) < 20)) and (
                (abs(blue - kJ1[0]) < 10 and abs(green - kJ1[1]) < 35 and abs(red - kJ1[2]) < 30)
            or (abs(blue - kJ3[0]) < 10 and abs(green - kJ3[1]) < 15
                and abs(red - kJ3[2]) < 10)):
        print("Classement du GrandPrix")
        video.gp.final_score_position = classement(video.frame, video.count)
        return True
    return False
