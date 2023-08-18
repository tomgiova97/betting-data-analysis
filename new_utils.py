from team_data import TeamData

ID = 'id'
SPORT_KEY = 'sport_key'
SPORT_TITLE = 'sport_title'
COMMENCE_TIME = 'commence_time'
HOME_TEAM = 'home_team'
AWAY_TEAM = 'away_team'
BOOKMAKER_KEY = 'bookmaker_key'
BOOKMAKER_TITLE = 'bookmaker_title'
HOME_WIN = 'home_win'
AWAY_WIN = 'away_win'
DRAW = 'draw'
OVER_2_5 = 'over_2_5'
UNDER_2_5 = 'under_2_5'
HOME_GOALS = 'home_goals'
AWAY_GOALS = 'away_goals'

def is_team_home(team_name, home_team):
    return team_name == home_team
    
def is_score_draw(home_goals, away_goals):
    return home_goals == away_goals

def is_team_winner(is_team_home, home_goals, away_goals):
    if (is_team_home):
        return home_goals > away_goals
    else:
        return home_goals < away_goals
    
def is_over_threshold(threshold, home_goals, away_goals):
    return home_goals + away_goals > threshold    
    
def calc_expected_outcomes(is_team_home, home_win_odd, away_win_odd, draw_odd, under_2_5_odd, over_2_5_odd):
    if (is_team_home):
        exp_win = 1./home_win_odd
        exp_defeat = 1./away_win_odd
        exp_draw = 1./draw_odd
        exp_under_2_5 = 1./under_2_5_odd
        exp_over_2_5 = 1./over_2_5_odd
        return exp_win, exp_defeat, exp_draw, exp_under_2_5, exp_over_2_5
    
    else :
        exp_win = 1./away_win_odd
        exp_defeat = 1./home_win_odd
        exp_draw = 1./draw_odd
        exp_under_2_5 = 1./under_2_5_odd
        exp_over_2_5 = 1./over_2_5_odd
        return exp_win, exp_defeat, exp_draw, exp_under_2_5, exp_over_2_5

def calc_team_data(team_name, team_df):
    dates = []
    wins = []
    exp_wins = []
    draws = []
    exp_draws = []
    defeats = []
    exp_defeats = []
    under_2_5 = []
    exp_under_2_5 = []
    over_2_5 = []
    exp_over_2_5 = []

    for index, row in team_df.iterrows():
        dates.append(row[COMMENCE_TIME])
        is_match_home = is_team_home(team_name, row[HOME_TEAM])
        exp_outcomes = calc_expected_outcomes(is_match_home, row[HOME_WIN], row[AWAY_WIN]
                                              , row[DRAW], row[UNDER_2_5], row[OVER_2_5])
        exp_wins.append(exp_outcomes[0])
        exp_defeats.append(exp_outcomes[1])
        exp_draws.append(exp_outcomes[2])
        exp_under_2_5.append(exp_outcomes[3])
        exp_over_2_5.append(exp_outcomes[4])

        # Evaluating the number of goals scored 
        if (is_over_threshold(2.5, row[HOME_GOALS], row[AWAY_GOALS])):
            under_2_5.append(0)
            over_2_5.append(1)
        else: 
            under_2_5.append(1)
            over_2_5.append(0)

        # Evaluating the match outcome 
        if (is_score_draw(row[HOME_GOALS], row[AWAY_GOALS])):
            wins.append(0)
            defeats.append(0)
            draws.append(1)
        else:
            if (is_team_winner(is_match_home, row[HOME_GOALS], row[AWAY_GOALS])):
                wins.append(1)
                defeats.append(0)
                draws.append(0)
            else :
                wins.append(0)
                defeats.append(1)
                draws.append(0)

   ## Collect all the data found to create a TeamDate object
    team_data = TeamData(team_name, dates, wins, defeats, draws, exp_wins, exp_defeats, exp_draws, under_2_5, over_2_5, exp_under_2_5, exp_over_2_5 )

    return team_data

def gen_df_columns_dictionary(df, col_names):
    col_dictionary = {}
    col_list = df.columns.tolist()    
    for i in range(0, len(col_names)):
        col_dictionary[col_names[i]] = col_list[i]

    return col_dictionary     

