class Run:
    def __init__(self, nb_player):
        self.nb_player = nb_player
        self.positions_data = [[]*self.nb_player]
        self.items_data = [[] * self.nb_player]
        self.players_statut_data = [[1] * self.nb_player]
        self.timers_data = [[] * self.nb_player]
        self.classement_data = [[] * self.nb_player]
        self.level_name = None

