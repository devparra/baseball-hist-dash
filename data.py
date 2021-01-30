# Import bootstrap, dash-html, pandas
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

# Import CSV data
teams = pd.read_csv('data/team.csv')
batters = pd.read_csv('data/batting.csv')
players = pd.read_csv('data/player.csv')

# Hardcoded list of era names as key value pairs
era_list = [{'label': 'Dead Ball (\'03-\'19)','value': 'Dead Ball'},
            {'label': 'Live Ball (\'20-\'41)','value': 'Live Ball'},
            {'label': 'Integration (\'42-\'60)','value': 'Integration'},
            {'label': 'Expantion (\'61-\'76)','value': 'Expantion'},
            {'label': 'Free Agency (\'77-\'93)','value': 'Free Agency'},
            {'label': 'Steroid (\'94-\'05)','value': 'Steroid'},
            {'label': 'Post-Steroid (\'06-\'15)','value': 'Post-Steroid'}]

era_marks = {
                1903: {'label': '1903'},
                1919: {'label': '1919'},
                1941: {'label': '1941'},
                1960: {'label': '1960'},
                1976: {'label': '1976'},
                1993: {'label': '1993'},
                2005: {'label': '2005'},
                2015: {'label': '2015'},
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
    filter_team_yr = teams[['year','name']]
    # filter the above list by year span
    filter_year = filter_team_yr[(filter_team_yr.year >= era_time[x][0])&(filter_team_yr.year <= era_time[x][1])] # High Year
    # filter_year = filter_year[] # Low Year
    # Create a filter list of Team names based on years filtered
    filter_teams = filter_year['name'].unique()
    # return unique list of team names as a list of key value pairs, rather than calling a function to create and return the list
    # list comp of key value pair
    # new is a list of names while x is the name in the list
    return [{'label': x, 'value': x} for x in filter_teams]


def dynamicrange(x):
    # Hardcoded data is not typically what i do unless the set is small
    era_time = [(1903,1919),
                (1920,1941),
                (1942,1960),
                (1961,1976),
                (1977,1993),
                (1994,2005),
                (2006,2015)]
    return [era_time[x][0],era_time[x][1]]
