# import dash IO and graph objects
from dash.dependencies import Input, Output
# Plotly graph objects to render graph plots
import plotly.graph_objects as go
# import plotly express
import plotly.express as px

# Import app
from app import app

# Import pandas and sqlite from data module
from data.data import pd, sl

# Import custom functions
from data.data import (dynamic_top, time_step, calculate_pa, calculate_trc, lag_method, 
    corr_method, est_games, batter_lr, car_avg)


# Triggered by html.P(id='none')
@app.callback(
    [Output('top-player-dropdown', 'options'),
    Output('top-player-dropdown', 'value')],
    [Input('none', 'children')])
def select_top_player(call):
    # Generate 100 players for 2022 season
    top_players = dynamic_top(2022)
    # Return player list
    return top_players, top_players[0]['value']


# Callback for Player profile datatable
@app.callback(
    [Output('top-player-info-tabel', 'data'),
     Output('top-player-info-tabel', 'columns')],
    [Input('top-player-dropdown', 'value')])
def update_top_profile(player):
    # SQL connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    player_data = pd.read_sql_query(f'''SELECT DISTINCT player.nameFirst || ' ' || player.nameLast AS playerName, fielder.pos, fielder.InnOuts,
                                            player.birth_date, player.bats, player.throws, debut
                                        FROM people player
                                            LEFT JOIN fielding fielder ON fielder.playerID = player.playerID
                                        WHERE player.playerID = '{player}';''',sqlite_con)
    sqlite_con.close()
    # Set player position to most played position
    player_data = player_data[player_data.InnOuts == player_data.InnOuts.max()]
    player_data.drop(['InnOuts'], inplace=True, axis=1)
    # return player data
    return player_data.to_dict('records'), [{'name': x, 'id': x} for x in player_data]


# Callback for player statistics
@app.callback(
    [Output('top-player-data-tabel', 'data'),
     Output('top-player-data-tabel', 'columns'),
     Output('intermediate-data', 'data')],
    [Input('top-player-dropdown', 'value')])
def update_top_data(player):
    # SQL connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    player_data = pd.read_sql_query(f'''SELECT DISTINCT batter.yearID, batter.G,
                                        batter.AB, batter.R, batter.H, "2B" AS double, "3B" AS triple, batter.HR, batter.RBI, batter.SB, batter.CS,
                                        batter.BB, batter.SO, batter.IBB, batter.HBP, batter.SH, batter.SF, batter.GIDP
                                    FROM batting batter
                                    WHERE batter.playerID = '{player}'
                                    ORDER BY batter.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    
    # Group statistics so players with multiple seasons are combined
    player_data = player_data.groupby(['yearID'],as_index=False).agg('sum').reset_index(drop=True)
    
    # Calculate statictics
    player_data['PA'] = player_data.pipe(calculate_pa)
    player_data['tRC'] = round(player_data.pipe(calculate_trc))

    #Drop unnecessary rows
    player_data.drop(['AB','H','BB','HBP','SH','SF','R','double','triple','HR','RBI','SB','CS','SO','IBB','GIDP'], inplace=True, axis=1)
    
    # Fill or replace any missing data
    player_data.fillna(0.0, inplace=True)
    player_data.replace({None: 0.0, '': 0.0}, inplace=True)
    player_data.reset_index(drop=True,inplace=True)
    
    # Return player stats
    return player_data.to_dict('records'), [{'name': x, 'id': x} for x in player_data], player_data.to_json(date_format='iso', orient='split')


# Player 162 game career average
@app.callback(
    [Output('top-player-caravg-tabel', 'data'),
     Output('top-player-caravg-tabel', 'columns')],
    [Input('intermediate-data', 'data')])
def update_carr_data(data):
    # read data from player stats datatable
    player_data = pd.read_json(data, orient='split')
    
    carr_avg = player_data.pipe(car_avg)

    # Return data
    return carr_avg.to_dict('records'), [{'name': x, 'id': x} for x in carr_avg]


# Player predicted statistics
@app.callback(
    [Output('top-player-pred-tabel', 'data'),
     Output('top-player-pred-tabel', 'columns')],
    [Input('intermediate-data', 'data'),Input('reg-dropdown', 'value'),
     Input('top-player-dropdown', 'value')])
def update_pred_data(data, method, player):
    # SQL connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    player_name = pd.read_sql_query(f'''SELECT IFNULL((player.nameFirst || ' ' || player.nameLast), SUBSTR(player.playerID,1,LENGTH(player.playerID)-3)) playerName
                                        FROM people player
                                        WHERE player.playerID = "{player}";''',sqlite_con)
    sqlite_con.close()

    # read data from player stats datatable
    player_data = pd.read_json(data, orient='split')
    # Establish player name in dataframe
    player_data['playerName'] = player_name.loc[0,'playerName']

    # Check method, adjust years selected based on method
    if method != 'Lag Method':
        player_data = player_data[(player_data.yearID <= 2022)&(player_data.yearID >= 2017)]
        player_data = player_data[player_data.yearID != 2020]
        player_data.fillna(0.0, inplace=True)
        player_data.replace({None: 0.0, '': 0.0}, inplace=True)
        player_data.reset_index(drop=True,inplace=True)
        player_predictions = player_data.pipe(batter_lr)
    else:
        player_data = player_data[(player_data.yearID <= 2022)&(player_data.yearID >= 2016)]
        player_data = player_data[player_data.yearID != 2020]
        player_data.fillna(0.0, inplace=True)
        player_data.replace({None: 0.0, '': 0.0}, inplace=True)
        player_data.reset_index(drop=True,inplace=True)
        player_predictions = player_data.pipe(batter_lr)
    # set predictions dataframe
    pred_data = player_predictions[method]
    # Drop player name
    pred_data.drop(['playerName'], inplace=True, axis=1)
    # Return data
    return pred_data.to_dict('records'), [{'name': x, 'id': x} for x in pred_data]


# Games Regression Callback
@app.callback(
    Output('g-regression', 'figure'),
    [Input('intermediate-data', 'data'),Input('reg-dropdown', 'value')])
def update_g_regression(data, method):
    # retrieve data from player stats datatable
    player_data = pd.read_json(data, orient='split')
    # set regression method series
    # call method in series by name
    reg_select = pd.Series(data=[time_step, lag_method, est_games], index=['Time Step', 'Lag Method', 'Corr Method'])
    # set figure
    fig1 = go.Figure()
    # select method
    if method == 'Time Step':
        player_data = player_data[(player_data.yearID >=2017)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        player_reg = player_data.pipe(reg_select[method],'G')
        # plotly express returns value error, possible due to no data available yet
        try:
            ols_line = px.scatter(x=player_reg[2].index, y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            # if value error, try again, this is a hack to force an express graph into a plotly object
            ols_line = px.scatter(x=player_reg[2].index, y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig1.add_trace(ols_line.data[1])
        fig1.add_trace(go.Scatter(name='Test', x=player_reg[1].index, y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig1.add_trace(go.Scatter(name='Train', x=player_reg[2].index, y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig1.update_xaxes(title='Time Step')
    elif method == 'Lag Method':
        player_data = player_data[(player_data.yearID >=2016)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        player_reg = player_data.pipe(reg_select[method],'G')
        try:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig1.add_trace(ols_line.data[1])
        fig1.add_trace(go.Scatter(name='Test', x=player_reg[3], y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig1.add_trace(go.Scatter(name='Train', x=player_reg[3], y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig1.update_xaxes(title='Lag')
    else:
        # If Correlation method selected
        # Player game are calculated rather than correlated
        player_data = player_data[(player_data.yearID >=2017)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        # Set horizontal line to establish 50th quantile
        # fig1.add_hline(y=player_data.G.median(), line_width=2.5, line_dash="solid", line_color="Blue", opacity=0.25)
        fig1.add_trace(go.Scatter(name='Median', x=player_data.index, y=[player_data.G.median() for i in player_data.index], hovertemplate = 'Median: %{y}<extra></extra><br>', mode='none', fill='tonexty', fillcolor='#ffc447', fillpattern=dict(shape='x', fgcolor='dodgerblue')))
        fig1.add_trace(go.Scatter(name='Games', x=player_data.index, y=player_data.G, hovertemplate = 'Games: %{y}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
    # Set options, return figure
    fig1.update_yaxes(title='G')
    fig1.update_layout(title="Games Regression",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    fig1.update_layout(hovermode="x", height=500, width=775)
    return fig1


# Plate-Apperences Regression Callback
@app.callback(
    Output('pa-regression', 'figure'),
    [Input('intermediate-data', 'data'),Input('reg-dropdown', 'value')])
def update_pa_regression(data, method):
    # Read player statistics from datatable
    player_data = pd.read_json(data, orient='split')
    # set regression method series
    reg_select = pd.Series(data=[time_step, lag_method, corr_method], index=['Time Step', 'Lag Method', 'Corr Method'])
    # Set figure
    fig2 = go.Figure()
    # Select method, same as above
    if method == 'Time Step':
        player_data = player_data[(player_data.yearID >=2017)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        player_reg = player_data.pipe(reg_select[method],'PA')
        # Hack method to get plotly express to fit into a plotly object
        try:
            ols_line = px.scatter(x=player_reg[2].index, y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[2].index, y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig2.add_trace(ols_line.data[1])
        fig2.add_trace(go.Scatter(name='Test', x=player_reg[1].index, y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig2.add_trace(go.Scatter(name='Train', x=player_reg[2].index, y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig2.update_xaxes(title='Time Step')
    elif method == 'Lag Method':
        player_data = player_data[(player_data.yearID >=2016)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        player_reg = player_data.pipe(reg_select[method],'PA')
        try:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig2.add_trace(ols_line.data[1])
        fig2.add_trace(go.Scatter(name='Test', x=player_reg[3], y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig2.add_trace(go.Scatter(name='Train', x=player_reg[3], y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig2.update_xaxes(title='Lag')
    else:
        player_data = player_data[(player_data.yearID >=2017)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        game_est = player_data.pipe(est_games)
        player_reg = player_data.pipe(reg_select[method],'G', 'PA', game_est)
        try:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig2.add_trace(ols_line.data[1])
        fig2.add_trace(go.Scatter(name='Test', x=player_reg[3], y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig2.add_trace(go.Scatter(name='Train', x=player_reg[3], y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig2.update_xaxes(title='G')
    # Set graph options and return
    fig2.update_yaxes(title='PA')
    fig2.update_layout(title="Plate Apperences Regression",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    fig2.update_layout(hovermode="x", height=500, width=775)
    return fig2


# Runs Created callback
@app.callback(
    Output('trc-regression', 'figure'),
    [Input('intermediate-data', 'data'),Input('reg-dropdown', 'value')])
def update_trc_regression(data, method):
    # get player stats from datatable
    player_data = pd.read_json(data, orient='split')
    # regression selection
    reg_select = pd.Series(data=[time_step, lag_method, corr_method], index=['Time Step', 'Lag Method', 'Corr Method'])
    # Set figure
    fig3 = go.Figure()
    # select method
    if method == 'Time Step':
        player_data = player_data[(player_data.yearID >=2017)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        player_reg = player_data.pipe(reg_select[method],'tRC')
        # plotly express hack
        try:
            ols_line = px.scatter(x=player_reg[2].index, y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[2].index, y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig3.add_trace(ols_line.data[1])
        fig3.add_trace(go.Scatter(name='Test', x=player_reg[1].index, y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig3.add_trace(go.Scatter(name='Train', x=player_reg[2].index, y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig3.update_xaxes(title='Time Step')
    elif method == 'Lag Method':
        player_data = player_data[(player_data.yearID >=2016)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        player_reg = player_data.pipe(reg_select[method],'tRC')
        try:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig3.add_trace(ols_line.data[1])
        fig3.add_trace(go.Scatter(name='Test', x=player_reg[3], y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig3.add_trace(go.Scatter(name='Train', x=player_reg[3], y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig3.update_xaxes(title='Lag')
    else:
        player_data = player_data[(player_data.yearID >=2017)&(player_data.yearID != 2020)]
        player_data.reset_index(drop=True,inplace=True)
        game_est = player_data.pipe(est_games)
        pa_pred = player_data.pipe(reg_select[method],'G', 'PA', game_est)
        player_reg = player_data.pipe(reg_select[method],'PA', 'tRC', pa_pred[0])
        try:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        except ValueError:
            ols_line = px.scatter(x=player_reg[3], y=player_reg[2], trendline='ols', trendline_color_override='lightblue')
        fig3.add_trace(ols_line.data[1])
        fig3.add_trace(go.Scatter(name='Test', x=player_reg[3], y=player_reg[1], hovertemplate = 'Predicted: %{y}<extra></extra><br>', mode='markers', marker_color='Orange', opacity=0.8, marker=dict(size=10)))
        fig3.add_trace(go.Scatter(name='Train', x=player_reg[3], y=player_reg[2], hovertemplate = 'Actual: %{y:.0f}<extra></extra><br>', mode='markers', marker_color='Green', opacity=0.6, marker=dict(size=8)))
        fig3.update_xaxes(title='PA')
    # Set options, return
    fig3.update_yaxes(title='tRC')
    fig3.update_layout(title="Technical Runs Created Regression",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    fig3.update_layout(hovermode="x", height=500, width=775)
    return fig3