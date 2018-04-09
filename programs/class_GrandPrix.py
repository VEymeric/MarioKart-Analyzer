from class_run import *


class GrandPrix:
    def __init__(self):
        self.nb_player = None
        self.final_score_points = None
        self.final_score_position = None
        self.run = None
        self.state = 0

    def begin(self, nb_player):
        self.nb_player = nb_player
        self.final_score_points = [0] * nb_player
        self.final_score_position = [0] * nb_player
        self.run = []

    def start_run(self, level_name):
        self.run.append(Run(self.nb_player, level_name))

    def get_last_run(self):
        if len(self.run) == 0:
            print("ERROR no run detected")
            return None
        else:
            return self.run[len(self.run)-1]


if __name__ == "__main__":
    x = GrandPrix()
    x.begin(4)
    print(x.final_score_points)
    x.run.append(Run(x.nb_player, "lol"))
    print(x.run[0].classement_data)
    x.state = 2
    print(x.state)
    test = x.get_last_run()
    print(test.level_name)

