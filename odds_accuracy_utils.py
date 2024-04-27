import math

HOME_WIN = 'home_win'
AWAY_WIN = 'away_win'
DRAW = 'draw'
HOME_GOALS = 'home_goals'
AWAY_GOALS = 'away_goals'

def get_match_outcome(match_row):
    home_goals = match_row[HOME_GOALS]
    away_goals = match_row[AWAY_GOALS]

    if home_goals > away_goals:
        return "1"
    elif home_goals < away_goals:
        return "2"
    elif home_goals == away_goals:
        return "X"
    else: raise Exception(f"Error in calculating score for match {match_row['id']}")

def get_match_total_goals(match_row):
    home_goals = match_row[HOME_GOALS]
    away_goals = match_row[AWAY_GOALS]    
    return home_goals + away_goals

def get_bin_index(low_bin_limit, upp_bin_limit, bins_step, value):
    if (value < upp_bin_limit):
        index = round((value - low_bin_limit)/bins_step, 2)
        return math.floor(index)
    
def get_double_chance_odd(odd_1, odd_2):
    return (odd_1 * odd_2) / (odd_1 + odd_2)    
    

# Insert h2h expected and real result for a single event
# If only_home is True, only the home odds are taken into account 
def fill_h2h_bins(bins, match_score, home_win_bin_index, away_win_bin_index, draw_bin_index
              , home_win_odd, away_win_odd, draw_odd, only_home = False):

    if (home_win_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT
        bins[home_win_bin_index].append([1./home_win_odd, match_score == "1"])

    if ((not only_home) and away_win_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT
        bins[away_win_bin_index].append([1./away_win_odd, match_score == "2"])

    if (draw_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT    
        bins[draw_bin_index].append([1./draw_odd, match_score == "X"])

    return bins    

# It's the opposite of the previous method when only_home = True 
def fill_h2h_bins_for_away_events(bins, match_score, home_win_bin_index, away_win_bin_index, draw_bin_index
              , home_win_odd, away_win_odd, draw_odd):
        
    if (away_win_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT
        bins[away_win_bin_index].append([1./away_win_odd, match_score == "2"])

    if (draw_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT    
        bins[draw_bin_index].append([1./draw_odd, match_score == "X"])

    return bins  
    

def fill_totals_bins(bins, match_total_goals, over_2_5_bin_index, under_2_5_bin_index
              , over_2_5_odd, under_2_5_odd):

    if (over_2_5_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT
        bins[over_2_5_bin_index].append([1./over_2_5_odd, match_total_goals > 2.5])

    if (under_2_5_bin_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT
        bins[under_2_5_bin_index].append([1./under_2_5_odd, match_total_goals < 2.5])

    return bins      


def fill_double_chance_bins(bins, match_score, d_c_index, d_c_odd, is_double_chance_in):

    if (d_c_index!=None): # Can be None if odd is higher than UPP_ODD_LIMIT
        if(is_double_chance_in):
            bins[d_c_index].append([1./d_c_odd, (match_score == "1" or match_score == "X")])
        else:
            bins[d_c_index].append([1./d_c_odd, (match_score == "2" or match_score == "X")])    

    return bins        