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

    def change_les_points(self, joueur, nb_point):
        self.classement_data[joueur] +=  nb_point

    def timers(self, logger):
        values = []
        logger.info("laps time  :  %s", self.timers_data)
        min_laps = self.timers_data[0][-1]
        for player in range(self.nb_player):
            if(min_laps > self.timers_data[player][-1]):
                min_laps = self.timers_data[player][-1]
        for player in range(self.nb_player):
            logger.info("Final time  :  J%s: +%3s", player+1, self.timers_data[player][-1]-min_laps)

        return values
