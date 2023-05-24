# Import Pandas
import pandas as pd
# Import Numpy
import numpy as np
# Import SQLite 3
import sqlite3 as sl


# Hardcoded list of era names as key value pairs
era_list = [{'label': 'Statcast (\'16-PRES)','value': 'Statcast'},
            {'label': 'Post-Steroid (\'06-\'15)','value': 'Post-Steroid'},
            {'label': 'Steroid (\'94-\'05)','value': 'Steroid'},
            {'label': 'Free Agency (\'77-\'93)','value': 'Free Agency'},
            {'label': 'Expantion (\'61-\'76)','value': 'Expantion'},
            {'label': 'Integration (\'42-\'60)','value': 'Integration'},
            {'label': 'Live Ball (\'20-\'41)','value': 'Live Ball'},
            {'label': 'Dead Ball (\'03-\'19)','value': 'Dead Ball'},
            {'label': 'Knickerbocker (\'71-\'02)','value': 'Knickerbocker'}]

# Hardcoded list of era names only
era_marks = ['Statcast','Post-Steroid','Steroid','Free Agency',
    'Expantion','Integration','Live Ball','Dead Ball','Knickerbocker']

# Hardcoded list of era ranges as tuples
era_time = [(2016,2022),
            (2006,2015),
            (1994,2005),
            (1977,1993),
            (1961,1976),
            (1942,1960),
            (1920,1941),
            (1903,1919),
            (1871,1902)]


# Dyname League Generator
def dynamicleagues(e):
    '''
    Generate league ids based on selected era.

    e: string
        Selected era
    
    Return: key-value pair
        league ID's
    '''
    # Import Hardcoded lists
    global era_time
    global era_marks
    # SQL connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # No assertion for the variable e is needed
    # League ID data
    leagues = pd.read_sql_query(f'''SELECT DISTINCT lgID
                                        FROM teams team
                                    WHERE team.yearID >= {era_time[era_marks.index(e)][0]} AND team.yearID <= {era_time[era_marks.index(e)][1]}
                                    ORDER BY team.yearID ASC;''', sqlite_con)
    sqlite_con.close()
    # return list comp of key value pair
    return [{'label': k, 'value': v }for k, v in zip(leagues['lgID'], leagues['lgID'])]


# Dynamic Team Names
def dynamicteams(e,l):
    '''
    Generate team names based on era and league.

    e: string
        Selcted era

    l: string
        Selected league

    Return: key-value pair
        Team names only
    '''
    # Hardcoded lists
    global era_time
    global era_marks
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team name data
    filter_team_ids = pd.read_sql_query(f'''SELECT DISTINCT team.name
                                        FROM teams team
                                        WHERE team.lgID = "{l}" AND team.yearID >= {era_time[era_marks.index(e)][0]} AND team.yearID <= {era_time[era_marks.index(e)][1]}
                                        ORDER BY team.yearID ASC;''', sqlite_con)
    sqlite_con.close()
    # return list comp of key value pair
    return [{'label': k, 'value': v }for k, v in zip(filter_team_ids['name'], filter_team_ids['name'])]


# Dynamic Years
def dynamicyears(team, years):
    '''
    Dynamically generate a list of active years based on team and year (era) span.

    team: string
        Team name

    years: list
        Years span.

    Returns: key-value pair
        Years within range
    '''
    # SQL connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # selected year span base on team
    year_data = pd.read_sql_query(f'''SELECT team.yearID
                                FROM teams team
                                WHERE team.name = "{team}"
                                    AND team.yearID >= {years[0]}
                                    AND team.yearID <= {years[1]}
                                ORDER BY team.yearID DESC;''',sqlite_con)
    sqlite_con.close()
    # return list comp of key value pair
    return [{'label': k, 'value': v }for k, v in zip(year_data['yearID'], year_data['yearID'])]


# Dynamic Year Range
def dynamicrange(e):
    '''
    Dynamically generate an array of years an era spans.

    e: string
        Selcted era

    Return: list
        Year range
    '''
    # Hardcoded data
    global era_time
    global era_marks
    # return year range
    return [era_time[era_marks.index(e)][0],era_time[era_marks.index(e)][1]]


# Dynamic Roster Generator
def dynamicplayers(pos,team,year):
    '''
    Dynamically generate a short roster of players based on postion, team, and roster year.

    pos: string
        Player position
    
    team: string
        Player team
    
    year: int
        Roster year

    Return: Key-Value Pair
        Player Names and ID's
    '''
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # select team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                        FROM teams team
                                        WHERE name = "{team}"
                                            AND yearID = {year};''',sqlite_con)
    # query database for players names and ids
    player_list = pd.read_sql_query(f'''SELECT fielder.playerID, IFNULL((player.nameFirst || ' ' || player.nameLast), SUBSTR(fielder.playerID,1,LENGTH(fielder.playerID)-3)) playerName
                                FROM fielding fielder
                                    LEFT JOIN people player ON player.playerID = fielder.playerID
                                WHERE fielder.teamID = "{select_team_id['teamID'][0]}"
                                    AND fielder.yearID = {year}
                                    AND fielder.pos = "{pos}"
                                ORDER BY fielder.playerID ASC;''',sqlite_con)
    sqlite_con.close()
    # delete dataframe to save memory
    del select_team_id
    # Return key value list of players names with ids
    return [{'label': k, 'value': v }for k, v in zip(player_list.playerName, player_list.playerID)]


# Calculate Technical Runs Created
def calculate_trc(df):
    '''
    Information on Technical Runs Created can be found here: https://blogs.fangraphs.com/get-to-know-runs-created/
    
    Prior to 1955 some stats where not maintained
    Technical Runs Created can be calculated using:
      ((H + BB - CS + HBP - GDP) * ((1B + (2*2B) + (3*3B) + (4*HR) + (.26 * (BB - IBB + HBP)) + (.52 * (SH + SF + SB)))))/ (AB + BB + HBP + SF + SH)

    df: pandas.dataframe
        Player Data

    Return: pandas.dataframe
        Technical Runs Created
    '''
    # Fill any NA with 0
    df.fillna(0)
    # Set variables for calculation of total bases
    SNG = (((df.H - df.double) - df.triple) - df.HR)
    DBL = 2 * df.double
    TPL = 3 * df.triple
    HR = 4 * df.HR
    # Total bases
    TB = (SNG + DBL + TPL + HR)
    # Calculate Runs Created
    calc_1 = (df.H + df.BB - df.CS + df.HBP - df.GIDP) 
    calc_2 = .26 * (df.BB - df.IBB + df.HBP)
    calc_3 = .52 * (df.SH + df.SF + df.SB)
    calc_4 = (df.AB + df.BB + df.HBP + df.SH + df.SF)
    # delete dataframe to save space
    del df
    try:
        # return calculation
        return (((calc_1)*((TB)+(calc_2)+(calc_3)))/(calc_4))
    except ZeroDivisionError :
        # if error return 0
        return 0
    

# Calculate Plate Apperences
def calculate_pa(df):
    '''
    Calculate Plate Apperences

    df: pandas.dataframe
        Player data

    Return: pandas.dataframe
        Plate Apperences
    '''
    # fill na with 0
    df.fillna(0)
    # set variables
    ab = df.AB
    bb = df.BB
    hbp = df.HBP
    sf = df.SF
    sh = df.SH
    # delete dataframe
    del df
    # return calculation
    return ab + bb + hbp + sf + sh


# Calculate On-Base Percentage
def calculate_obp(df):
    '''
    Calculate On-Base Percentage

    df: pandas.dataframe
        Player data 

    Return: pandas.dataframe
        On-Base Percentage
    '''
    # fill NA with 0
    df.fillna(0)
    # Set variables
    AB = df.AB
    Ht = df.H
    BB = df.BB
    HBP = df.HBP
    SF = df.SF
    # delete dataframe
    del df
    try:
        # return On-Base Percentage
        return (Ht + BB + HBP) / (AB + BB + HBP + SF)
    except ZeroDivisionError :
        # if error return 0
        return 0


# Calculate Slugging Average
def calculate_slg(df):
    '''
    Calculate Slugging Average

    df: pandas.dataframe
        Player data

    Return: pandas.dataframe
        Slugging Average
    '''
    # fill na with 0
    df.fillna(0)
    # Set variables
    AB = df.AB
    Ht = df.H
    DBL = df.double
    TRP = df.triple
    HR = df.HR
    # delete dataframe
    del df
    # calculate singles
    SNG = Ht - DBL - TRP - HR
    try:
        # return Slugging Average
        return (SNG + 2*DBL + 3*TRP + 4*HR)/AB
    except ZeroDivisionError :
        # if error return 0
        return 0


# Calculate Batting Average on Balls In PLay
def calculate_babip(df):
    '''
    Calculate Batting Average on Balls In PLay

    df: pandas.dataframe
        Player data

    Return: pandas.dataframe
        Calculated BABIP
    '''
    # fill NA with 0
    df.fillna(0)
    # Set variables
    AB = df.AB
    Ht = df.H
    SO = df.SO
    HR = df.HR
    # delete dataframe
    del df
    try:
        # return babip
        return (Ht - HR) / (AB - SO - HR)
    except ZeroDivisionError :
        # if error return 0
        return 0


# Calculate Basic Runs Created
def calculate_brc(df):
    '''
    Information on Basic Runs Created can be found here: https://blogs.fangraphs.com/get-to-know-runs-created/
    
    Prior to 1955 some stats where not maintained
    Basic Runs Created can be calculated using:
      (Hits + Walks) * (Total Bases) / (At Bats + Walks)

    df: pandas.dataframe
        Player data

    Returns: pandas.dataframe
        Basic Runs Created
    '''
    # fill NA with 0
    df.fillna(0)
    # Set variables
    SNG = df.H - df.double - df.triple - df.HR
    DBL = 2*df.double
    TPL = 3*df.triple
    HR = 4*df.HR
    # calculate total bases
    TB = (SNG + DBL + TPL + HR)
    # simple calculations
    calc_1 = (df.H + df.BB)
    calc_2 = (df.AB + df.BB)
    try:
        # return basic runs created
        return ((calc_1) * (TB) / (calc_2))
    except ZeroDivisionError :
        # if error return 0
        return 0


# Career Average
def car_avg(df):
    '''
    Provides a 162 game career average.

    df: pandas.DataFrame
        player data, int or float only
    
    Returns: pandas.DataFrame
        162 game career average.
    '''
    # Create copy
    carr = df.copy()
    # fill NA with 0
    carr.fillna(0)
    # generate factor
    fact = round(carr.G.sum()/162,4)
    # sum players career in own row
    carr.loc['Career_Avg'] = carr.sum(axis=0)
    # Apply factor
    carr = carr.apply(lambda x : round(x/fact))
    # Set Games to 162
    carr['G'] = '162 avg.'
    # Set year
    carr['yearID'] = df.yearID.max()
    # delete data to save memory
    del df
    # return last row, row with career average
    return carr[-1:]


# Typically this would be an import to a library such as SKLearn
# I just wanted to show a coded implementation
class LinearRegression:
    '''
    This is an OLS single variate regression.

    fit: int
        Takes a series as X and Y. Calculates and sets Intercept, Slope and Coefficient.
    
    coefficient: 
        Returns the amount that a change in x must be multiplied by to achieve 
        the equivalent average change in y, or the amount that y changes for every 
        unit increase in x.
    
    score:
        Returns R^2, the statistical parameter that estimates the amount of variation 
        in the dependent variable that can be explained by the independent variable.
    
    slope:
        Returns the regression's slope, showing the steepness of the correlation.
    
    predict: int
        Takes in an indipendent variable to calculate and return the next value 
        using the slope-intercept formula.
    '''
    def __init__(self):
        # initialize the class with 0
        Intercept = 0
        Slope = 0
        Coef = 0
        self.Intercept = Intercept
        self.Slope = Slope
        self.Coef = Coef

    def fit(self, x, y):
        '''
        Fits the linear model.

        Takes in an array or series as X and Y
        
        X: int
            Training data, explanatory variable
        Y: int
            Target values, dependent variable

        Sets the Intercept, Slope, and Coefficent of the regression
        '''
        x_mean = x.mean()
        y_mean = y.mean()
        #slope
        slope_num = ((x - x_mean) * (y - y_mean)).sum()
        slope_den = ((x - x_mean)**2).sum()
        slope = slope_num / slope_den
        #intercept
        inter = y_mean - (slope * x_mean)
        # correlation coefficent
        N = np.prod(x.shape)
        corr_num = (N * (x*y).sum()) - (x.sum() * y.sum())
        corr_den = np.sqrt((N * (x**2).sum() - x.sum()**2) * (N * (y**2).sum() - y.sum()**2))
        r = corr_num / corr_den
        # return intercept, slope, and coefficent
        LinearRegression.Intercept=inter
        LinearRegression.Slope=slope
        LinearRegression.Coef=r
    
    # Although plotly will automatically supply this data
    # I thought it would only be appropitate to provide 
    # these functions for later use
    def coefficient(self):
        '''
        Returns the coefficent of the regression
        '''
        return LinearRegression.Coef
    
    def score(self):
        '''
        Returns the R^2 of the regression
        '''
        # Square the coefficent
        return LinearRegression.Coef**2
    
    def slope(self):
        '''
        Returns the slope of the regression
        '''
        return LinearRegression.Slope
    
    # Really the most important for this application
    def predict(self, x):
        '''
        Calculates the next dependent value.

        x: int
            Independent variable, can also be a series or array

        Returns the next predicted value.
        '''
        inter = LinearRegression.Intercept
        slope = LinearRegression.Slope
        # slope-intercept
        prediction = inter + slope * x
        # return predicted value
        return prediction


def est_games(df):
    '''
    Estimates the number of games a player will play. Assumes the player will start
    the season healthy and capable of playing all 162 games. Does not consider past 
    injuries or trades.

    df: pandas.dataframe
        Player data, games played

    The median (second quartile) is used to determain the seasons with the best 
    performance. Only values above the median are kept and an additonal 162 game 
    season is added to ensure a players 'peak' season can be estimated. Finally, 
    the players season is estimated with a weighted average.

    Return: int
        Estimate of predicted 'peak' games played
    '''
    games = df.G.copy()
    # Obtain upper 50%
    upper = games.median()
    up_games = games[games > upper]
    # save memory
    del upper
    # Add a 162 game season to ensure season cap
    games = pd.concat([pd.Series([162]),up_games])
    # save memory
    del up_games
    # Sort to establish weights
    games.sort_values(inplace=True)
    # Use the position of the sort as weight, highest protity goes to lagrest
    games.reset_index(drop=True,inplace=True)
    # return weighted average
    return round(np.average(games, weights=games.index))


def time_step(df,pred):
    '''
    This function conducts a linear regression using a Time-step. Time-step features 
    are those that can be calculated directly from the time index. The time dummy 
    is the most fundamental time-step feature, ticking off time steps in the series 
    from start to finish. You may mimic time dependency using time-step characteristics. 
    If the values of a series may be predicted based on when they occur, the series is 
    time dependent.

    df: pandas.dataframe

    pred: string
        Column that will be used in the calculation as the dependent variable

    Return: list
        prediction: int
        y_prediction: pandas.Series
        y: pandas.Series

    For our purpose this will apply directly to the baseball data in this application.
    '''
    step_data = df.copy()
    # obtain a list of years
    year_list = [year for year in enumerate(step_data.yearID.unique(), start=1)]
    # create labels for epochs
    for i, year in year_list:
        step_data.loc[step_data.yearID == year, "epoch"] = i
    step_data.reset_index(drop=True,inplace=True)
    # regression
    X = step_data.loc[:,['epoch']]
    y = step_data.loc[:, pred]
    del step_data
    regression = LinearRegression()
    regression.fit(X.epoch, y)
    # predictions
    predictions = {xid: round(regression.predict(x)) for xid, x in enumerate(X.epoch[:])}
    y_predictions = pd.Series(predictions)
    # if column is "games", cap at 162
    if pred == 'G':
        prediction = 162 if regression.predict(int(X.epoch.max()+1)) > 162 else regression.predict(int(X.epoch.max()+1))
    else:
        prediction = regression.predict(int(X.epoch.max()+1))
    # return list
    return [prediction, y_predictions, y]


def lag_method(df,pred):
    '''
    This function conducts a linear regression using a lag feature. For a lag function, 
    we relocate the target series observations to make them seem later in time. 
    We will use a 1-step lag function. You may mimic serial dependency using lag features. 
    A time series exhibits serial dependency when an observation can be anticipated based 
    on previous observations.

    df: pandas.dataframe

    pred: string
        Column that will be used in the calculation as the dependent variable

    Return: list
        prediction: int
        y_prediction: pandas.Series
        y: pandas.Series
        X.lag: pandas.Series
    
    For our purpose this will apply directly to the baseball data in this application.
    '''
    lag_data = df.copy()
    # delete data to save memory
    del df
    # lag feature
    lag_data['lag'] = lag_data[pred].shift(1)
    lag_data.dropna(inplace=True)
    lag_data.reset_index(drop=True,inplace=True)
    # regression
    X = lag_data.loc[:,['lag']]
    y = lag_data.loc[:, pred]
    y, X = y.align(X, join='inner')
    regression = LinearRegression()
    regression.fit(X.lag, y)
    # predictions
    predictions = {xid: round(regression.predict(x)) for xid, x in enumerate(X.lag[:])}
    y_predictions = pd.Series(predictions)
    # if column is "games", cap at 162
    if pred == 'G':
        prediction = 162 if regression.predict(lag_data[pred].tail(1).values[0]) > 162 else regression.predict(lag_data[pred].tail(1).values[0])
    else:
        prediction = regression.predict(lag_data[pred].tail(1).values[0])
    # delete data to improve memory
    del lag_data
    # return list
    return [prediction, y_predictions, y, X.lag]


def corr_method(df,feat,pred,inde):
    '''
    This function conducts a linear regression, correlating two features. The most common 
    methodologies for investigating the relationship between two quantitative variables 
    are correlation and linear regression. Correlation evaluates the strength of a 
    linear connection between two variables, whereas regression mathematically 
    defines the relationship.
    
    df: pandas.dataframe

    feat: string
        Column that will be used in the calculation as the explanatory variable

    pred: string
        Column that will be used in the calculation as the dependent variable
    
    inde: int
        Independent variable to predict

    Return: list
        prediction: int
        y_prediction: pandas.Series
        y: pandas.Series
        X[feat]: pandas.Series
    
    For our purpose this will apply directly to the baseball data in this application.
    '''
    # Correlation features
    X = df.loc[:,[feat]].copy()
    y = df.loc[:, pred].copy()
    # delete data to save memory
    del df
    # Regression
    regression = LinearRegression()
    regression.fit(X[feat], y)
    # predictions
    predictions = {xid: round(regression.predict(x)) for xid, x in enumerate(X[feat][:])}
    y_predictions = pd.Series(predictions)
    prediction = regression.predict(inde)
    # return list
    return [prediction, y_predictions, y, X[feat]]


# may get turned into a class later
def batter_lr(df):
    '''
    Packages all regression methods into one fucntion. Very specific to this application.

    df: pandas.Dataframe
        Player data

    Return: dictionary
        A dictionary of dataframes that provide predictions on player data.
    '''
    # Correlation
    predict_games = df.pipe(est_games)
    pa_cor_data = df.pipe(corr_method, 'G', 'PA', predict_games)
    rc_cor_data = df.pipe(corr_method, 'PA', 'tRC', pa_cor_data[0])
    player_cor_pred = pd.DataFrame({'YearEst': df.yearID.max()+1, 'playerName': df.playerName.unique(), 'G': predict_games, 'PA': round(pa_cor_data[0]), 'tRC': round(rc_cor_data[0])},index=[0])
    
    # time-step
    g_time_data = df.pipe(time_step,'G')
    pa_time_data = df.pipe(time_step,'PA')
    rc_time_data = df.pipe(time_step,'tRC')    
    player_time_pred = pd.DataFrame({'YearEst': df.yearID.max()+1, 'playerName': df.playerName.unique(), 'G': round(g_time_data[0]), 'PA': round(pa_time_data[0]), 'tRC': round(rc_time_data[0])},index=[0])
    
    # lag
    g_lag_data = df.pipe(lag_method,'G')
    pa_lag_data = df.pipe(lag_method,'PA')
    rc_lag_data = df.pipe(lag_method,'tRC')
    player_lag_pred = pd.DataFrame({'YearEst': df.yearID.max()+1, 'playerName': df.playerName.unique(), 'G': round(g_lag_data[0]), 'PA': round(pa_lag_data[0]), 'tRC': round(rc_lag_data[0])},index=[0])
    
    # delete data to save memory
    del df
    
    # Package into dictionary
    player_results = {'Corr Method':player_cor_pred, 'Time Step':player_time_pred, 'Lag Method':player_lag_pred}
    
    # Return resulting predictions dictionary
    return player_results


def dynamic_top(year):
    '''
    Generates a list of the top 100 baseball players. Queries the Lahman database for player 
    data whom have played in the past 10 years (from the year selected). Players who have played 
    less than 7 years are dropped. Players who have played less than 2/3 of the selected season 
    will be dropped. Players are sorted by Games played,  PA (Plate Apperences), and tRC (Technical Runs Created). 

    year: int
        Selected year for top players

    Return: key-value pair
        Provides player names and id's
    '''
    # SQL connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # query database for players name, id, and stats
    player_data = pd.read_sql_query(f'''SELECT DISTINCT batter.yearID, player.nameFirst || ' ' || player.nameLast AS playerName, player.playerID,
                                        batter.G, batter.AB, batter.R, batter.H, "2B" AS double, "3B" AS triple, batter.HR, batter.RBI, batter.SB, batter.CS,
                                        batter.BB, batter.SO, batter.IBB, batter.HBP, batter.SH, batter.SF, batter.GIDP
                                    FROM batting batter
                                        LEFT JOIN fielding fielder ON fielder.playerID = batter.playerID
                                        LEFT JOIN people player ON player.playerID = batter.playerID
                                    WHERE batter.yearID >= {(year - 7)} AND fielder.pos != 'P'
                                    ORDER BY batter.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # group by to aggregate players with multiple teams into one season
    player_data = player_data.groupby(['yearID','playerName','playerID'],as_index=False).agg('sum').reset_index(drop=True)
    # calculate defining statistics
    player_data['PA'] = player_data.pipe(calculate_pa)
    player_data['tRC'] = round(player_data.pipe(calculate_trc))
    player_data.drop(['AB','H','BB','HBP','SH','SF','R','double','triple','HR','RBI','SB','CS','SO','IBB','GIDP'], inplace=True, axis=1)

    # Count the number of occurences, determains career length
    counts = player_data['playerName'].value_counts()
    # Filter the counts by comparing occurences to 7
    player_data = player_data[~player_data['playerName'].isin(counts[counts < 7].index)]

    # Select only the choice season
    player_list = player_data[player_data.yearID == year].copy()
    
    # delete data to save memory
    del player_data, counts
    # players who have played more than 2/3 season (108 games)
    player_list = player_list[player_list.G > 108]
    # players who have played the most games
    player_list.sort_values('G', ascending=False, inplace=True)
    # players who have had the most PA, more opportunities to score a run
    player_list.sort_values('PA', ascending=False, inplace=True)
    # players with the highest technical runs created, biggest runs contribution
    player_list.sort_values('tRC', ascending=False, inplace=True)
    player_list.reset_index(drop=True,inplace=True)
    # Top 100 players
    player_list = player_list.loc[:, ['playerName','playerID']]
    player_list = player_list.iloc[:100]

    # Return key value list of players names with id
    return [{'label': k, 'value': v }for k, v in zip(player_list.playerName, player_list.playerID)]