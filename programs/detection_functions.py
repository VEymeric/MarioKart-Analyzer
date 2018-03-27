from images_functions import *


def is_loading(state, mini_gray, loading_screen, count):
    if compare_images_value(mini_gray, loading_screen) < 2:
        print(str(count) + " : loading :" + str(compare_images_value(mini_gray, loading_screen)))
        # check if we are in a real loading
        # cv2.imwrite("../ressources/miniframe/%d.jpg" % count, frame)  # save frame as JPEG file
        return state + 1
    # print(compare_images_value(mini_gray, loading_screen))
    return state


def is_end_of_loading(state, mini_gray, loading_screen, count):
    if compare_images_value(mini_gray, loading_screen) > 10:
        # print(str(count) + " : end loading")
        # cv2.imwrite("../ressources/tests/%d.jpg" % count, frame)  # save frame as JPEG file
        return state + 1, count
    return state, 0


def level_name(state, count, last_frame, mini_gray, frame):
    if count == (last_frame + 30):
        score, name = score_compare_image_and_folder("../ressources/miniframe/valide", mini_gray)
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


def run_detection(state, count, last_frame):
    if count == (last_frame + 100):
        # if(comparaisonObjet("../ressources/Objets", gray_frame)):
        # cv2.imwrite("../ressources/test2/" + str(count) + ".jpg", gray_frame)  # save frame as JPEG file
        return state + 1
    return state


def end_of_run_detection(state):
    return 0


if __name__ == "__main__":
    loading = "../ressources/miniframe/720.jpg"
    loadind = cv2.imread(loading)
    loading = cv2.cvtColor(loading, cv2.COLOR_BGR2GRAY)
    loading2 = "yolo.jpg"
    #loading = cv2.imread(loading)
    loading2 = cv2.imread(loading2)

    screen = "../ressources/test/1600.jpg"
    test = cv2.imread(screen)[0:100]
    print(compare_images_value(loading, test))
    print(compare_images_value(test, loading))
    print(compare_images_value(loading2, test))
    print(compare_images_value(test, loading2))
    print(compare_images_value(loading, loading2))
