class Run:
    def __init__(self, nb_player, level):
        self.nb_player = nb_player
        self.positions_data = []
        self.timers_data = []
        self.items_data = []
        self.classement_data = []

        for i in range(self.nb_player):
            self.positions_data.append([])
            self.timers_data.append([])
            self.items_data.append([])
            self.classement_data.append([])

        self.players_statut_data = [[1] * self.nb_player]
        self.level_name = level
