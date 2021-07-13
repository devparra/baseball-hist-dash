# Improtant note: This data file would ordinarily be used to connect with a proper database server
# more likely PostgreSQL, but thats me. I do plan on rewritting this in the future for such implementations.
# With that said, this file will be be very slow to run and only to demonstrate data processing using
# functions and pandas along with providing a central file for data references
#
# Import Pandas
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Import CSV data
# Import team historical statistics
# Some historical team names are correlated with their more modern counter part
# Custome CSV files where created from the original by combining data to allow
# for easier display of historical team data
teams = pd.read_csv('data/update_team.csv')
# Import Players batting data
batters = pd.read_csv('data/update_batting.csv')
# Import custom Fielding data
fielding = pd.read_csv('data/update_fielding.csv')
# Import custom pitching data
pitching = pd.read_csv('data/update_pitching.csv')
# Import Player profile data
players = pd.read_csv('data/update_player.csv')
# Import custom player and team id dataframe
team_players = pd.read_csv('data/player_team.csv')

batters.fillna(0,inplace=True)
fielding.fillna(0,inplace=True)
pitching.fillna(0,inplace=True)

# Hardcoded list of era names as key value pairs
era_list = [{'label': 'Dead Ball (\'03-\'19)','value': 'Dead Ball'},
            {'label': 'Live Ball (\'20-\'41)','value': 'Live Ball'},
            {'label': 'Integration (\'42-\'60)','value': 'Integration'},
            {'label': 'Expantion (\'61-\'76)','value': 'Expantion'},
            {'label': 'Free Agency (\'77-\'93)','value': 'Free Agency'},
            {'label': 'Steroid (\'94-\'05)','value': 'Steroid'},
            {'label': 'Post-Steroid (\'06-\'15)','value': 'Post-Steroid'},
            {'label': 'Statcast (\'16-\'20)','value': 'Statcast'}]

# Era markers
era_marks = {
                1903: {'label': '1903',},
                1919: {'label': '1919',},
                1941: {'label': '1941',},
                1960: {'label': '1960',},
                1976: {'label': '1976',},
                1993: {'label': '1993',},
                2005: {'label': '2005',},
                2015: {'label': '2015',},
                2020: {'label': '2020',}
            }


# Creates a dynamic list of team names based on era
def dynamicteams(x):
    # Hardcoded list of era time spans, wouldnt do it this way if the set where larger
    era_time = [(1903,1919),
                (1920,1941),
                (1942,1960),
                (1961,1976),
                (1977,1993),
                (1994,2005),
                (2006,2015),
                (2016,2020)]
    # create a filter list of just years and team names
    filter_team_yr = teams[['year','name','team_id']]
    # filter the above list by year span
    filter_year = filter_team_yr[(filter_team_yr.year >= era_time[x][0])&(filter_team_yr.year <= era_time[x][1])] # High Year
    # filter_year = filter_year[] # Low Year
    # Create a filter list of Team names based on years filtered
    filter_teams = filter_year['name'].unique()
    filter_team_ids = filter_year['team_id'].unique()
    # return unique list of team names as a list of key value pairs, rather than calling a function to create and return the list
    # list comp of key value pair
    # new is a list of names while x is the name in the list
    return [{'label': k, 'value': v }for k, v in zip(filter_teams, filter_team_ids)]



def dynamicrange(x):
    # Hardcoded data is not typically what i do unless the set is small
    era_time = [(1903,1919),
                (1920,1941),
                (1942,1960),
                (1961,1976),
                (1977,1993),
                (1994,2005),
                (2006,2015),
                (2016,2020)]
    return [era_time[x][0],era_time[x][1]]


# Calculate Estimate Plate Appearence
def calculate_pa(df):
    ab = df.ab
    bb = df.bb
    hbp = df.hbp
    sf = df.sf
    sh = df.sh
    return ab + bb + hbp + sf + sh


# Calculate On-Base Percentage function
def calculate_obp(df):
    # Set lists of team data
    AB = df.ab
    Ht = df.h
    BB = df.bb
    HBP = df.hbp
    SF = df.sf
    # return On-Base Percentage
    try:
        return (Ht + BB + HBP) / (AB + BB + HBP + SF)
    except ZeroDivisionError :
        return 0


# Calculate Slugging Average
def calculate_slg(df):
    # Set lists of player data
    AB = df.ab
    Ht = df.h
    DBL = df.double
    TRP = df.triple
    HR = df.hr
    SNG = Ht - DBL - TRP - HR
    # return Slugging Average
    try:
        return (SNG + 2*DBL + 3*TRP + 4*HR)/AB
    except ZeroDivisionError :
        return 0


# Calculate OPS
def calculate_ops(df):
    slg = df.slg
    obp = df.obp
    return obp + slg


# Basic
# (H+BB)*(TB)/(AB+BB)
def calculate_brc(df):
    SNG = df.h - df.double - df.triple - df.hr
    DBL = 2*df.double
    TPL = 3*df.triple
    HR = 4*df.hr
    TB = (SNG + DBL + TPL + HR)
    calc_1 = (df.h + df.bb)
    calc_2 = (df.ab + df.bb)
    try:
        return ((calc_1) * (TB) / (calc_2))
    except ZeroDivisionError :
        return 0


# Stolen Base
# (H+BB-CS)*(TB+(.55*SB))/(AB+BB)
def calculate_sbrc(df):
    SNG = df.h - df.double - df.triple - df.hr
    DBL = 2*df.double
    TPL = 3*df.triple
    HR = 4*df.hr
    TB = (SNG + DBL + TPL + HR)
    calc_1 = (df.h + df.bb - df.cs)
    calc_2 = .55 * df.sb
    calc_3 = df.ab + df.bb
    try:
        return (((calc_1) * ((TB) + (calc_2))) / calc_3)
    except ZeroDivisionError :
        return 0


# Technical
# (H+BB-CS+HBP-GIDP)*(TB+(.26*(BB-IBB+HBP))+(.52*(SH+SF+SB)))/(AB+BB+HBP+SH+SF)
def calculate_trc(df):
    SNG = df.h - df.double - df.triple - df.hr
    DBL = 2 * df.double
    TPL = 3 * df.triple
    HR = 4 * df.hr
    TB = (SNG + DBL + TPL + HR)
    calc_1 = (df.h + df.bb - df.cs + df.hbp - df.g_idp) 
    calc_2 = .26 * (df.bb - df.ibb + df.hbp)
    calc_3 = .52 * (df.sh + df.sf + df.sb)
    calc_4 = (df.ab + df.bb + df.hbp + df.sh + df.sf)
    try:
        return (((calc_1)*((TB)+(calc_2)+(calc_3)))/(calc_4))
    except ZeroDivisionError :
        return 0


def year_factor(df):
    column_names = df.columns
    df_copy = df.copy()
    mask = df_copy['year'] == 2020
    for n, c in enumerate(column_names):
        if n <= 4:
            pass
        else:
            df_copy.loc[mask, c] = df_copy.loc[mask, c].apply(lambda x: round(x*2.7))
    return df_copy


def player_project(data, player):
    
    # Calculate the average At-Bats per Game played in a season
    def ab_rate(df):
        return df.ab / df.g
    
    # Calculate Estimate Plate Appearence
    def calc_pa(df):
        ab = df.ab
        bb = df.bb
        hbp = df.hbp
        sf = df.sf
        sh = df.sh
        return ab + bb + hbp + sf + sh

    # Calculate On-Base Percentage
    def calc_obp(df):
        AB = df.ab
        Ht = df.h
        BB = df.bb
        HBP = df.hbp
        SF = df.sf
        try:
            return (Ht + BB + HBP) / (AB + BB + HBP + SF)
        except ZeroDivisionError :
            return 0

    # Calculate Slugging Average
    def calc_slg(df):
        AB = df.ab
        Ht = df.h
        DBL = df.double
        TRP = df.triple
        HR = df.hr
        SNG = Ht - DBL - TRP - HR
        try:
            return (SNG + 2*DBL + 3*TRP + 4*HR)/AB
        except ZeroDivisionError :
            return 0

    # Calculate OPS
    def calc_ops(df):
        slg = df.slg
        obp = df.obp
        return obp + slg

    # Basic
    # (H+BB)*(TB)/(AB+BB)
    def calc_brc(df):
        SNG = df.h - df.double - df.triple - df.hr
        DBL = 2*df.double
        TPL = 3*df.triple
        HR = 4*df.hr
        TB = (SNG + DBL + TPL + HR)
        calc_1 = (df.h + df.bb)
        calc_2 = (df.ab + df.bb)
        try:
            return ((calc_1) * (TB) / (calc_2))
        except ZeroDivisionError :
            return 0

    # Stolen Base
    # (H+BB-CS)*(TB+(.55*SB))/(AB+BB)
    def calc_sbrc(df):
        SNG = df.h - df.double - df.triple - df.hr
        DBL = 2*df.double
        TPL = 3*df.triple
        HR = 4*df.hr
        TB = (SNG + DBL + TPL + HR)
        calc_1 = (df.h + df.bb - df.cs)
        calc_2 = .55 * df.sb
        calc_3 = df.ab + df.bb
        try:
            return (((calc_1) * ((TB) + (calc_2))) / calc_3)
        except ZeroDivisionError :
            return 0
    
    # Technical
    # (H+BB-CS+HBP-GIDP)*(TB+(.26*(BB-IBB+HBP))+(.52*(SH+SF+SB)))/(AB+BB+HBP+SH+SF)
    def calc_trc(df):
        SNG = df.h - df.double - df.triple - df.hr
        DBL = 2 * df.double
        TPL = 3 * df.triple
        HR = 4 * df.hr
        TB = (SNG + DBL + TPL + HR)
        calc_1 = (df.h + df.bb - df.cs + df.hbp - df.g_idp) 
        calc_2 = .26 * (df.bb - df.ibb + df.hbp)
        calc_3 = .52 * (df.sh + df.sf + df.sb)
        calc_4 = (df.ab + df.bb + df.hbp + df.sh + df.sf)
        try:
            return (((calc_1)*((TB)+(calc_2)+(calc_3)))/(calc_4))
        except ZeroDivisionError :
            return 0


    player_data = data[data.player_id == player]

    player_data = player_data.groupby(['year']).sum().reset_index()
    

    proj_games = round(np.average(player_data['g'], weights=player_data['g']))
    player_data['rate'] = player_data.apply(ab_rate,axis=1)
    player_ab_rate = np.average(player_data['rate'], weights=player_data['g'])
    proj_ab = round(proj_games * player_ab_rate)

    if (player_data.ab[0] == 0):
        proj_r = round(np.average(player_data['r']))
        proj_h = round(np.average(player_data['h']))
        proj_rbi = round(np.average(player_data['rbi']))
        proj_bb = round(np.average(player_data['bb']))
        proj_so = round(np.average(player_data['so']))
        proj_ibb = round(np.average(player_data['ibb']))
        proj_hbp = round(np.average(player_data['hbp']))
        proj_sh = round(np.average(player_data['sh']))
        proj_sf = round(np.average(player_data['sf']))
        proj_gidp = round(np.average(player_data['g_idp']))
    else:
        proj_r = round(np.average(player_data['r'], weights=player_data['ab']))
        proj_h = round(np.average(player_data['h'], weights=player_data['ab']))
        proj_rbi = round(np.average(player_data['rbi'], weights=player_data['ab']))
        proj_bb = round(np.average(player_data['bb'], weights=player_data['ab']))
        proj_so = round(np.average(player_data['so'], weights=player_data['ab']))
        proj_ibb = round(np.average(player_data['ibb'], weights=player_data['ab']))
        proj_hbp = round(np.average(player_data['hbp'], weights=player_data['ab']))
        proj_sh = round(np.average(player_data['sh'], weights=player_data['ab']))
        proj_sf = round(np.average(player_data['sf'], weights=player_data['ab']))
        proj_gidp = round(np.average(player_data['g_idp'], weights=player_data['ab']))
    
    if (player_data.h[0] == 0):
        proj_dbl = round(np.average(player_data['double']))
        proj_trp = round(np.average(player_data['triple']))
        proj_hr = round(np.average(player_data['hr']))
        proj_sb = round(np.average(player_data['sb']))
        proj_cs = round(np.average(player_data['cs']))
    else:
        proj_dbl = round(np.average(player_data['double'], weights=player_data['h']))
        proj_trp = round(np.average(player_data['triple'], weights=player_data['h']))
        proj_hr = round(np.average(player_data['hr'], weights=player_data['h']))
        proj_sb = round(np.average(player_data['sb'], weights=player_data['h']))
        proj_cs = round(np.average(player_data['cs'], weights=player_data['h']))

    predictions = np.array([[player, 2021, 1, 'PROJ', '--', proj_games, proj_ab, proj_r, proj_h, 
        proj_dbl, proj_trp, proj_hr, proj_rbi, proj_sb, proj_cs, proj_bb, proj_so, proj_ibb, 
        proj_hbp, proj_sh, proj_sf, proj_gidp]], dtype=object)
    
    pred_col = data.columns

    player_projection = pd.DataFrame(predictions, columns=pred_col)

    player_projection['pa'] = player_projection.apply(calc_pa,axis=1)
    player_projection['obp'] = round(player_projection.apply(calc_obp,axis=1),3)
    player_projection['slg'] = round(player_projection.apply(calc_slg,axis=1),3)
    player_projection['ops'] = round(player_projection.apply(calc_ops,axis=1),3)
    player_projection['t_rc'] = round(player_projection.apply(calc_trc,axis=1))
    player_projection['b_rc'] = round(player_projection.apply(calc_brc,axis=1))
    player_projection['s_rc'] = round(player_projection.apply(calc_sbrc,axis=1))

    player_projection = player_projection.astype({"year":'int64',"stint":'int64',"g":'int64', 
        "ab":'int64', "ab":'int64', "h":'int64', "r":'int64', "double":'int64',"triple":'int64', 
        "hr":'int64', "rbi":'int64', "sb":'int64', "cs":'int64',"bb":'int64', "so":'int64', 
        "ibb":'int64',"hbp":'int64',"sh":'int64', "pa":'int64', "sf":'int64', "g_idp":'int64', 
        "t_rc":'int64',"b_rc":'int64',"s_rc":'int64'})
    
    return player_projection


def player_lr_eval(df,player):

    def player_lrce(df,c):
        X = df.year.values.reshape(-1,1)
        y = df[c].values.reshape(-1,1)
        player_reg = LinearRegression().fit(X,y)
        if c == 'obp':
            return_value = player_reg.coef_
            return return_value[0][0] * 1000
        if c == 'slg':
            return_value = player_reg.coef_
            return return_value[0][0] * 1000
        if c == 'ops':
            return_value = player_reg.coef_
            return return_value[0][0] * 1000
        else:
            return_value = player_reg.coef_
            return return_value[0][0]
    
    column_names = df.columns

    df_copy = df.copy()
    df_copy = df_copy.groupby(['year']).sum().reset_index()
    
    data = [player,2021,1,'EVAL','--']
    
    for n, c in enumerate(column_names):
        if n <= 4:
            pass
        else:
            value = player_lrce(df_copy,c)
            data.append(value)

    df_copy['player_id'] = player
    df_copy['team_id'] = df.team_id
    df_copy['league_id'] = df.league_id
    
    # shift column 'Name' to first position
    first_col = df_copy.pop('player_id')
    fourth_col = df_copy.pop('team_id')
    fifth_col = df_copy.pop('league_id')
    
    # insert column using insert(position,column_name,
    # first_column) function
    df_copy.insert(0, 'player_id', first_col)
    df_copy.insert(3, 'team_id', fourth_col)
    df_copy.insert(4, 'league_id', fifth_col)

    df_copy.loc[len(df_copy.index)] = data

    return df_copy