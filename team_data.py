class TeamData:

    # def __init__(self, wins, defeats, draws, exp_wins, exp_defeats, exp_draws, over_2_5, under_2_5, exp_over_2_5, exp_under_2_5):
    #     self.wins = wins
    #     self.defeats = defeats
    #     self.draws = draws
    #     self.exp_wins = exp_wins
    #     self.exp_defeats = exp_defeats
    #     self.exp_draws = exp_draws
    #     self.over_2_5 = over_2_5
    #     self.under_2_5 = under_2_5
    #     self.exp_over_2_5 = exp_over_2_5
    #     self.exp_under_2_5 = exp_under_2_5


    def __init__(self, team_name):
        self.team_name = team_name
        self.wins = 0.
        self.defeats = 0.
        self.draws = 0.
        self.exp_wins = 0.
        self.exp_defeats = 0.
        self.exp_draws = 0.
        self.over_2_5 = 0.
        self.under_2_5 = 0.
        self.exp_over_2_5 = 0.
        self.exp_under_2_5 = 0.
        
    def __str__(self):
        attributes = [
            f"team_name: {self.team_name}",
            f"wins: {self.wins}",
            f"defeats: {self.defeats}",
            f"draws: {self.draws}",
            f"exp_wins: {self.exp_wins}",
            f"exp_defeats: {self.exp_defeats}",
            f"exp_draws: {self.exp_draws}",
            f"over_2_5: {self.over_2_5}",
            f"under_2_5: {self.under_2_5}",
            f"exp_over_2_5: {self.exp_over_2_5}",
            f"exp_under_2_5: {self.exp_under_2_5}"
        ]
        return f"TeamData({', '.join(attributes)})"        