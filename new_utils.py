from team_data import TeamData
from datetime import datetime

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

def calc_team_data(team_name, team_df, only_home = False):
    dates = []
    matches_home=[]
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
        matches_home.append(convert_boolean_to_int(is_match_home))
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
    team_data = TeamData(team_name, dates, matches_home, wins, defeats, draws, exp_wins, exp_defeats, exp_draws, under_2_5, over_2_5, exp_under_2_5, exp_over_2_5 )

    return team_data

def convert_boolean_to_int(boolean):
    if(boolean):
        return 1
    else:
        return 0

def gen_df_columns_dictionary(df, col_names):
    col_dictionary = {}
    col_list = df.columns.tolist()    
    for i in range(0, len(col_names)):
        col_dictionary[col_names[i]] = col_list[i]

    return col_dictionary     


def convert_date_format(input_date_string):
    input_date_format = "%Y-%m-%dT%H:%M:%SZ"
    output_date_format = "%d/%m/%y"
    
    # Convert the input date string to a datetime object
    input_date = datetime.strptime(input_date_string, input_date_format)
    
    # Format the datetime object to the desired output format
    output_date_string = input_date.strftime(output_date_format)
    
    return output_date_string

def calculate_list_cumulative_values(list):
    cum_list = []
    cum_sum = 0.

    for element in list:
        cum_sum+=element
        cum_list.append(cum_sum)
    return cum_list    

def calculate_normalized_difference(cumulative_list, reference_list):
    if len(cumulative_list) != len(reference_list):
        raise Exception("Input lists are not the same size")
    
    cumulative_values = calculate_list_cumulative_values(cumulative_list)
    normalized_diff_list = []

    for i in range(len(cumulative_list)):
        normalized_diff_list.append(cumulative_values[i] - reference_list[i])

    return normalized_diff_list

# Calculate the ratio (cumulative) between the gained and the wagered money 
# If only_home=True, only the home matches are considered
def calculate_cumulative_gain_ratio(act_wins, exp_wins, matches_home, only_home=False):
    if ((len(act_wins) != len(exp_wins)) or (len(act_wins) != len(matches_home)) ):
        raise Exception("Input lists have not the same dimension")
    
    cum_gain_ratio = []
    cum_gain = 0.
    counter = 0.
    for i in range(len(act_wins)):        
        if ((not only_home) or (matches_home[i]==1)):
            counter += 1
            win_odd = 1./exp_wins[i]
            cum_gain += act_wins[i]*win_odd
            cum_gain_ratio.append((cum_gain)/(counter))

    return cum_gain_ratio    
