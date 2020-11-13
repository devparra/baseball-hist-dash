# Import pandas
import pandas as pd
import numpy as np

# Import CSV data
teams = pd.read_csv('data/team.csv')

# Hardcoded list of era names as key value pairs
era_list = [{'label': 'Dead Ball (\'03-\'19)','value': 'Dead Ball'},
            {'label': 'Live Ball (\'20-\'41)','value': 'Live Ball'},
            {'label': 'Integration (\'42-\'60)','value': 'Integration'},
            {'label': 'Expantion (\'61-\'76)','value': 'Expantion'},
            {'label': 'Free Agency (\'71-\'93)','value': 'Free Agency'},
            {'label': 'Steroid (\'94-\'05)','value': 'Steroid'},
            {'label': 'Post-Steroid (\'06-\'15)','value': 'Post-Steroid'}]


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
    # return unique list of team names as a list of key value pairs
    return listpair(filter_teams)


def dynamicrange(x):
    # Hardcoded data is not typically what i do unless the set is small
    era_time = [(1903,1919),
                (1920,1941),
                (1942,1960),
                (1961,1976),
                (1977,1993),
                (1994,2005),
                (2006,2015)]
    filter_range = [era_time[x][0],era_time[x][1]]
    return filter_range
