# Import pandas
import pandas as pd

# Import CSV data
teams = pd.read_csv('data/team.csv')

# Hardcoded list of era names as key value pairs
era_list = [{'label': 'Dead Ball','value': 'Dead Ball'},
            {'label': 'Live Ball','value': 'Live Ball'},
            {'label': 'Integration','value': 'Integration'},
            {'label': 'Expantion','value': 'Expantion'},
            {'label': 'Free Agency','value': 'Free Agency'},
            {'label': 'Steroid','value': 'Steroid'},
            {'label': 'Post-Steroid','value': 'Post-Steroid'}]


# Creates a list of key value pairs in the format:
# [{'label': <LABLE>, 'value': <VALUE>}]
def listpair(new):
    # Establish empty dictionary and list
    _dict={}
    _dict_list=[]
    # set loop to iterate input list
    for i in range(len(new)):
        # assign lable and value in dictionary
        _dict['label'] = new[i]
        _dict['value'] = new[i]
        # add pair to list
        _dict_list.append(_dict.copy())
    # return a list of key value pairs
    return _dict_list


# Creates a dynamic list of team names based on era
def dynamicteams(x):
    # Hardcoded list of era time spans
    era_time = [(1903,1919),
                (1920,1941),
                (1942,1960),
                (1961,1976),
                (1977,1993),
                (1994,2005),
                (2005,2015)]
    # create a filter list of just years and team names
    filter_team_yr = teams[['year','name']]
    # filter the above list by year span
    filter_year = filter_team_yr[filter_team_yr.year <= era_time[x][1]] # High Year
    filter_year = filter_year[filter_year.year >= era_time[x][0]] # Low Year
    # Create a filter list of Team names based on years filtered
    filter_teams = filter_year['name'].unique()
    # return unique list of team names as a list of key value pairs
    return listpair(filter_teams)
