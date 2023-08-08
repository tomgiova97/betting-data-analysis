import pandas as pd

DATE = 'Date'
MATCH = 'Match'
HOME_GOALS = 'Home Goals'
AWAY_GOALS = 'Away Goals'
HOME_WIN_ODDS = '1 (Home Win) Odds'
DRAW_ODDS = 'X (Draw) Odds'
AWAY_WIN_ODDS = '2 (Away Win) Odds'
UNDER_2_5_ODDS = 'Under 2.5 Odds'
OVER_2_5_ODDS = 'Over 2.5 Odds'

def is_team_home(team_name, match):
    teams = match.split(' vs ')
    if (team_name not in teams):
        raise Exception('Given team name is not present in the given match')
    else:
        return team_name==teams[0]
    
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
    wins = 0
    exp_wins = 0
    draws = 0
    exp_draws = 0
    defeats = 0
    exp_defeats = 0
    under_2_5 = 0
    exp_under_2_5 = 0
    over_2_5 = 0
    exp_over_2_5 = 0

    for index, row in team_df.iterrows():
        is_match_home = is_team_home(team_name, row[MATCH])
        exp_outcomes = calc_expected_outcomes(is_match_home, row[HOME_WIN_ODDS], row[AWAY_WIN_ODDS]
                                              , row[DRAW_ODDS], row[UNDER_2_5_ODDS], row[OVER_2_5_ODDS])
        exp_wins += exp_outcomes[0]
        exp_defeats += exp_outcomes[1]
        exp_draws += exp_outcomes[2]
        exp_over_2_5 += exp_outcomes[3]
        exp_under_2_5 += exp_outcomes[4]

        if (is_over_threshold(2.5, row[HOME_GOALS], row[AWAY_GOALS])):
            over_2_5 += 1
        else: 
            under_2_5 += 1    

        if (is_score_draw(row[HOME_GOALS], row[AWAY_GOALS])):
            draws+=1
        else:
            if (is_team_winner(is_match_home, row[HOME_GOALS], row[AWAY_GOALS])):
                wins += 1    
            else :
                defeats += 1   

   ## Collect all the data found to create a TeamDate object (review the constructor and add to the csv file)

    return 0

def gen_df_columns_dictionary(df, col_names):
    col_dictionary = {}
    col_list = df.columns.tolist()    
    for i in range(0, len(col_names)):
        col_dictionary[col_names[i]] = col_list[i]

    return col_dictionary     

