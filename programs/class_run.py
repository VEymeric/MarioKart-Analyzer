class Run:
    def __init__(self, nb_player, level, frame_number):
        self.nb_player = nb_player
        self.positions_data = []
        self.timers_data = []
        self.items_data = []
        self.classement_data = [0]*nb_player

        for i in range(self.nb_player):
            self.positions_data.append([])
            self.timers_data.append([])
            self.items_data.append([])
            self.classement_data.append([])
        self.players_statut_data = [1] * self.nb_player
        self.level_name = level
        self.starting_frame = frame_number

    def set_classement_data(self, player, new_data):
        self.classement_data = new_data

    def timers(self):
        values = []
        print(self.timers_data)

        for player in range(self.nb_player):
            values.append([])
            if len(self.timers_data[player]) > 1:
                previous = self.timers_data[player][0]
                for t in self.timers_data[player][1:]:
                    if self.nb_player > 2:
                        values[player].append((t-previous)/30)
                    else:
                        values[player].append((t-previous)/60)
                    previous = t
        return values
