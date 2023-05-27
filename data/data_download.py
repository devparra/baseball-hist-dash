# M.Parra 5-27-23
# This script is used to import and update the lahman SQLite database
# provided by Webucator Training with the CSV data provided by the Chadwick Bureau.
# The only purpose is to update the database ONLY WITH THE DATA REQIRED TO RUN 
# THE MLB DATA EXPLORER APP. A much more comprehensive updater for this 
# database and this application will come at a later time.
#
# import the neccesary libraries
from sqlalchemy import create_engine
import sqlite3 as sl
import numpy as np
import pandas as pd
import requests
from zipfile import ZipFile
import os
import shutil


# Download URL of database
download_urls = ["https://github.com/WebucatorTraining/lahman-baseball-mysql/raw/master/lahmansbaseballdb.sqlite", 
                 "https://github.com/chadwickbureau/baseballdatabank/archive/refs/tags/v2023.1.zip"]

print('Downloads started ...')

for url in download_urls:
    # URLs to be downloaded
    response = requests.get(url)
    # send a HTTP request to the server and save
    # the HTTP response in a response object
    filename = url.split('/')[-1]
    with open(filename,'wb') as file:
        # write the contents of the response
        # to a new file in binary mode
        file.write(response.content)
        print (f'{filename} OK')

print('Downloads Complete.\n')

print('Extracting data from zipfile...')

# Unzip and extract CSV files
zip_file = ZipFile('v2023.1.zip', 'r')
zip_file.extractall('./')
zip_file.close()

print ('Extraction complete.\n')

print('Collecting data ...')

# Get the max year of the database
sqlite_con = sl.connect('lahmansbaseballdb.sqlite')
sql_year = pd.read_sql_query(f'''SELECT MAX(team.yearID) as Year
                                    FROM Teams team;''',sqlite_con)
sqlite_con.close()

# load CSV dataframes
teams_csv = pd.read_csv('./baseballdatabank-2023.1/core/Teams.csv')
people_csv = pd.read_csv('./baseballdatabank-2023.1/core/People.csv')
batting_csv = pd.read_csv('./baseballdatabank-2023.1/core/Batting.csv')
batting_post_csv = pd.read_csv('./baseballdatabank-2023.1/core/BattingPost.csv')
fielding_csv = pd.read_csv('./baseballdatabank-2023.1/core/Fielding.csv')
fielding_post_csv = pd.read_csv('./baseballdatabank-2023.1/core/FieldingPost.csv')
pitching_csv = pd.read_csv('./baseballdatabank-2023.1/core/Pitching.csv')
pitching_post_csv = pd.read_csv('./baseballdatabank-2023.1/core/PitchingPost.csv')
series_post_csv = pd.read_csv('./baseballdatabank-2023.1/core/SeriesPost.csv')
managers_csv = pd.read_csv('./baseballdatabank-2023.1/core/Managers.csv')
homegames_csv = pd.read_csv('./baseballdatabank-2023.1/core/HomeGames.csv')
allstar_csv = pd.read_csv('./baseballdatabank-2023.1/core/AllstarFull.csv')

print('Preping data ...')

# prepare teams data
teams_csv.insert(0,'ID', teams_csv.index+1, True)
teams_csv.insert(6,'div_ID', '', True)
teams_csv.insert(7,'teamRank', 0, True)
teams_csv.drop(columns=['Rank'],inplace=True)
teams_csv_data = teams_csv[teams_csv.yearID > sql_year.Year.iloc[0]].copy()
del teams_csv

# prepare peaople data
people_csv.drop(columns=['retroID', 'bbrefID'],inplace=True)
# create a date marker to import only new players
date_mark = pd.to_datetime(f'{sql_year.Year.iloc[0]+1}-01-01')
people_csv_data = people_csv[pd.to_datetime(people_csv['debut']) > date_mark].copy()
del people_csv

# prepare fielding data
fielding_csv.insert(0,'ID', fielding_csv.index+1, True)
fielding_csv.insert(5,'team_ID', 0.0, True)
fielding_csv_data = fielding_csv[fielding_csv.yearID > sql_year.Year.iloc[0]].copy()
del fielding_csv

# prepare pitching data
pitching_csv.insert(0,'ID', pitching_csv.index+1, True)
pitching_csv.insert(5,'team_ID', 0.0, True)
pitching_csv_data = pitching_csv[pitching_csv.yearID > sql_year.Year.iloc[0]].copy()
del pitching_csv

# prepare batting data
batting_csv.insert(0,'ID', batting_csv.index+1, True)
batting_csv.insert(5,'team_ID', 0.0, True)
batting_csv_data = batting_csv[batting_csv.yearID > sql_year.Year.iloc[0]].copy()
del batting_csv

# prepare fielding postseason csv data
fielding_post_csv.insert(0,'ID', np.nan, True)
fielding_post_csv.insert(5,'team_ID', 0.0, True)
fielding_post_csv_data = fielding_post_csv[fielding_post_csv.yearID > sql_year.Year.iloc[0]].copy()
del fielding_post_csv

# prepare postseason batting data
batting_post_csv.insert(0,'ID', batting_post_csv.index+1, True)
batting_post_csv.insert(5,'team_ID', 0.0, True)
batting_post_csv_data = batting_post_csv[batting_post_csv.yearID > sql_year.Year.iloc[0]].copy()
del batting_post_csv

# prepare postseason pitching data
pitching_post_csv.insert(0,'ID', pitching_post_csv.index+1, True)
pitching_post_csv.insert(5,'team_ID', 0.0, True)
pitching_post_csv_data = pitching_post_csv[pitching_post_csv.yearID > sql_year.Year.iloc[0]].copy()
del pitching_post_csv

# prepare postseason series data
series_post_csv.insert(0,'ID', series_post_csv.index+1, True)
series_post_csv.insert(5,'team_IDwinner', '', True)
series_post_csv.insert(7,'team_IDloser', '', True)
series_post_csv_data = series_post_csv[series_post_csv.yearID > sql_year.Year.iloc[0]].copy()
del series_post_csv

# prepare manager data
managers_csv.insert(0, 'ID', managers_csv.index+1, True)
managers_csv.insert(4,'team_ID', 0.0, True)
managers_csv.rename(columns={'rank':'teamRank'},inplace=True)
managers_csv_data = managers_csv[managers_csv.yearID > sql_year.Year.iloc[0]].copy()
del managers_csv

# prepare homegame data
homegames_csv.rename(columns={'year.key':'yearkey','league.key':'leaguekey','team.key':'teamkey',
                              'park.key':'parkkey','span.first':'spanfirst','span.last':'spanlast'},inplace=True)
homegames_csv.insert(0, 'ID', np.nan, True)
homegames_csv.insert(4,'team_ID', 0, True)
homegames_csv.insert(6,'park_ID', 0, True)
homegames_csv.insert(12,'spanfirst_date', '', True)
homegames_csv.insert(13,'spanlast_date', '', True)
homegames_csv_data = homegames_csv[homegames_csv.yearkey > sql_year.Year.iloc[0]].copy()
del homegames_csv

# prepare allstar data
allstar_csv.insert(0, 'ID', allstar_csv.index+1, True)
allstar_csv.insert(6, 'team_ID', 0, True)
allstar_csv_data = allstar_csv.copy()
del allstar_csv

# gather data
csv_data_list = [teams_csv_data, people_csv_data, batting_csv_data, batting_post_csv_data, fielding_csv_data, fielding_post_csv_data, 
            pitching_csv_data, pitching_post_csv_data, series_post_csv_data, managers_csv_data, homegames_csv_data, allstar_csv_data]

print('Updating SQL Database ...')

# set sql engine
engine = create_engine('sqlite:///lahmansbaseballdb.sqlite', echo=False)

# list sql tables to update
sql_table = ['teams','people','batting','battingpost','fielding','fieldingpost','pitching',
             'pitchingpost','seriespost','managers','homegames','allstarfull']

# loop over csv data tables
for i, csv_data in enumerate(csv_data_list):
    # update sql with csv
    print(f'Updating {sql_table[i]}')
    with engine.begin() as connection:
        # hack, unknown why cant update with just latest
        if sql_table[i] != 'allstarfull':
            exists = 'append'
        else:
            exists = 'replace'
        csv_data.to_sql(sql_table[i], con=connection, if_exists=exists, index=False)
    print(f'{sql_table[i]} OK')

print('SQL Database updated!\n')
print('Conducting cleanup ...')

# remove uneccesary files and folders
os.remove('v2023.1.zip')
shutil.rmtree('baseballdatabank-2023.1')

print('Cleanup complete! SQL Database is ready for use.')