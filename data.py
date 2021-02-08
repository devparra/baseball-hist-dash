# Improtant note: This data file would ordinarily be used to connect with a proper database server
# more likely PostgreSQL, but thats me. I do plan on rewritting this in the future for such implementations.
# With that said, this file will be be very slow to run and only to demonstrates data prep for processing using
# functions and pandas
import pandas as pd


# Import CSV data
# Import team historical statistics
# Replacements are used to allow for easier display of historical team data
# Some historical team names are correlated with their more modern counter part
# Im sure there is a better way, be back to this later
teams = pd.read_csv('data/team_update.csv')

# Import Players batting data
batters = pd.read_csv('data/batting.csv')

# Import Player profile data
players = pd.read_csv('data/player.csv')

team_players = pd.read_csv('data/player_team.csv')


# Hardcoded list of era names as key value pairs
era_list = [{'label': 'Dead Ball (\'03-\'19)','value': 'Dead Ball'},
            {'label': 'Live Ball (\'20-\'41)','value': 'Live Ball'},
            {'label': 'Integration (\'42-\'60)','value': 'Integration'},
            {'label': 'Expantion (\'61-\'76)','value': 'Expantion'},
            {'label': 'Free Agency (\'77-\'93)','value': 'Free Agency'},
            {'label': 'Steroid (\'94-\'05)','value': 'Steroid'},
            {'label': 'Post-Steroid (\'06-\'15)','value': 'Post-Steroid'}]

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
                (2006,2015)]

    # create a filter list of just years and team names
    filter_team_yr = teams[['year','name','team_id']]

    # filter the above list by year span
    filter_year = filter_team_yr[(filter_team_yr.year >= era_time[x][0])&(filter_team_yr.year <= era_time[x][1])]

    # Create a filter list of Team names and ids based on years filter
    filter_teams = filter_year['name'].unique()
    filter_team_ids = filter_year['team_id'].unique()

    # return unique list of team names and ids as a list of key value pairs
    return [{'label': k, 'value': v }for k, v in zip(filter_teams, filter_team_ids)]


def dynamicrange(x):
    # Hardcoded data is not typically what i would do unless the set is small
    era_time = [(1903,1919),
                (1920,1941),
                (1942,1960),
                (1961,1976),
                (1977,1993),
                (1994,2005),
                (2006,2015)]
    return [era_time[x][0],era_time[x][1]]


# Calculate On-Base Percentage function
def calculate_obp(data):
    # Set lists of team data
    AB = data.ab
    Ht = data.h
    BB = data.bb
    HBP = data.hbp
    SF = data.sf
    # return On-Base Percentage
    return (Ht + BB + HBP) / (AB + BB + HBP + SF)


# Calculate Slugging Average
def calculate_slg(data):
    # Set lists of player data
    AB = data.ab
    Ht = data.h
    DBL = data.double
    TRP = data.triple
    HR = data.hr
    SNG = Ht - DBL - TRP - HR
    # return Slugging Average
    return (SNG + 2*DBL + 3*TRP + 4*HR)/AB
