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
    
def calc_expected_outcomes(is_team_home, home_win_odd, away_win_odd, draw_odd):
    if (is_team_home):
        exp_win = 1./home_win_odd
        exp_defeat = 1./away_win_odd
        exp_draw = 1./draw_odd
        return exp_win, exp_defeat, exp_draw
    
    else :
        exp_win = 1./away_win_odd
        exp_defeat = 1./home_win_odd
        exp_draw = 1./draw_odd
        return exp_win, exp_defeat, exp_draw



    
