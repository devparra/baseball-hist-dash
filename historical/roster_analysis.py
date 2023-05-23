# import dash IO and graph objects
from dash.dependencies import Input, Output
# Plotly graph objects to render graph plots
import plotly.graph_objects as go
# Import dash html, bootstrap components, and tables for datatables
from dash import html, dash_table
# Import core components
from dash import dcc
# import bootstrap
import dash_bootstrap_components as dbc
import warnings

# Import app
from app import app

# Pandas and SQLite3
from data.data import pd, sl
# Custom functions
from data.data import (dynamicyears, dynamicleagues, dynamicplayers, 
                  dynamicteams, dynamicrange, calculate_trc, calculate_brc)


# This will update the league dropdown
@app.callback(
    [Output('league-select-dropdown', 'options'),
    Output('league-select-dropdown', 'value')],
    [Input('era-dropdown', 'value')])
def select_league_era(selected_era):
    # select era
    leagues = dynamicleagues(selected_era)
    # Return league list
    return leagues, leagues[0]['value']


# team dropdown callback
@app.callback(
    [Output('team-select-dropdown', 'options'),
    Output('team-select-dropdown', 'value')],
    [Input('era-dropdown', 'value'),Input('league-select-dropdown', 'value')])
def select_team_era(selected_era,selected_league):
    # select era and league
    teams = dynamicteams(selected_era,selected_league)
    # return team list
    return teams, teams[0]['value']


# Callback to year dropdown menu
@app.callback(
    [Output('year-select-dropdown', 'options'),Output('year-select-dropdown', 'value')],
    [Input('era-dropdown', 'value'),Input('team-select-dropdown', 'value')])
def update_year_dropdown(selected_era, selected_team):
    # select year range
    year_range = dynamicrange(selected_era)
    # selet year list base on range
    year_list = dynamicyears(selected_team, year_range)
    # Return list of active years for roster
    return year_list, year_list[0]['value']


# Select player position dropdown callback
@app.callback(
    [Output('pos-dropdown', 'options'), Output('pos-dropdown', 'value')],
    [Input('team-select-dropdown', 'value'),Input('year-select-dropdown', 'value')])
def update_pos_dropdown(selected_team, year):
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # get team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                            FROM teams team
                                            WHERE name = "{selected_team}"
                                                AND yearID = {year};''',sqlite_con)
    # get player postions for team and year
    postions = pd.read_sql_query(f'''SELECT DISTINCT Pos
                                FROM fielding fielder
                                WHERE teamID = '{select_team_id['teamID'][0]}'
                                    AND yearID = {year};''',sqlite_con)
    sqlite_con.close()
    # return a list of postions
    pos_list = [{'label': k, 'value': v }for k, v in zip(postions.POS, postions.POS)]

    # if no positions exist
    if not pos_list:
        # return empty list
        pos_list = [{'label': 'No Posions','value': 'None'}]

    # Return postion list
    return pos_list, pos_list[0]['value']


# Callback to player dropdown menu
@app.callback(
    [Output('player-dropdown', 'options'), Output('player-dropdown', 'value')],
    [Input('team-select-dropdown', 'value'),Input('year-select-dropdown', 'value'),
    Input('pos-dropdown', 'value')])
def update_player_dropdown(selected_team, year, select_pos):
    # generate player roster based on postion, team, and year
    team_roster = dynamicplayers(select_pos, selected_team, year)
    # If no one is in roster
    if not team_roster:
        # Return empty list
        team_roster = [{'label': 'No Roster','value': 'None'}]
    # Return roster
    return team_roster, team_roster[0]['value']


# Callback to Player profile datatable
@app.callback(
    [Output('player-data-tabel', 'children')],
    [Input('player-dropdown', 'value')])
def update_profile_table(player):
    # SQL connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    player_data = pd.read_sql_query(f'''SELECT DISTINCT player.nameFirst || ' ' || player.nameLast AS playerName, player.birth_date, player.bats, player.throws, debut
                                FROM people player
                                WHERE player.playerID = '{player}';''',sqlite_con)
    sqlite_con.close()
    # Set empty list
    data_note = []
    # if data filter is empty, append and return notice
    if player_data.empty:
        data_note.append(html.Div(dbc.Alert('No Player Data is available.', color='warning'),))
        return data_note
    # else set and return datatable
    else:
        data_note.append(html.Div(dash_table.DataTable(
            data= player_data.to_dict('records'),
            columns= [{'name': x, 'id': x} for x in player_data],
            style_as_list_view=True,
            editable=False,
            style_table={
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                },
        ),))
        return data_note


# Callback to Line Graph, takes data request from dropdown
@app.callback(
    Output('roster-rc-dist', 'figure'),
    [Input('team-select-dropdown', 'value'),
    Input('year-select-dropdown', 'value')])
def update_roster_rc(selected_team, year):
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # select team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                            FROM teams team
                                            WHERE name = "{selected_team}"
                                                AND yearID = {year};''',sqlite_con)
    # player roster with stats
    roster_rc = pd.read_sql_query(f'''SELECT DISTINCT player.nameFirst || ' ' || player.nameLast AS playerName,
                                        batter.AB, batter.R, batter.H, "2B" AS double, "3B" AS triple, batter.HR, batter.RBI, batter.SB, batter.CS,
                                        batter.BB, batter.SO, batter.IBB, batter.HBP, batter.SH, batter.SF, batter.GIDP
                                    FROM batting batter
                                        LEFT JOIN people player ON player.playerID = batter.playerID
                                        LEFT JOIN fielding fielder ON fielder.playerID = batter.playerID
                                    WHERE batter.teamID = "{select_team_id['teamID'][0]}"
                                        AND batter.yearID = {year}
                                        AND fielder.pos != "P";''',sqlite_con)
    sqlite_con.close()
    # if year is 1955 or greater, use Technical Runs Created
    if year >= 1955:
        roster_rc['RC'] = round(roster_rc.pipe(calculate_trc))
    # else use Basic Runs Created
    else:
        roster_rc['RC'] = round(roster_rc.pipe(calculate_brc))
    # fill and replace as needed
    roster_rc.fillna(0,inplace=True)
    roster_rc.replace({None: 0.0, '': 0.0}, inplace=True)
    roster_rc = roster_rc.astype({'RC': 'int'})
    # sort roster by runs created
    roster_rc = roster_rc.sort_values(['RC'],ascending=False)
    # Create Line char figure runs created
    rc_fig = go.Figure(data=[
        go.Bar(name='Runs Created',x=roster_rc.playerName, y=roster_rc.RC, hovertemplate = 'RC: %{y:}<extra></extra><br>', marker_color='#004687',opacity=0.8)
    ])
    # set graph options
    rc_fig.update_xaxes(title='Roster Position Players')
    rc_fig.update_yaxes(title='Runs Created', fixedrange=True)
    rc_fig.update_layout(title="Runs Created Distribution",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    rc_fig.update_layout(hovermode="x")
    # return graph
    return rc_fig


# Callback to Line Bubble Chart, take data request from dropdown menu
@app.callback(
    Output('roster-era-dist', 'figure'),
    [Input('team-select-dropdown', 'value'),
    Input('year-select-dropdown', 'value')])
def update_roster_era(selected_team, year):
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # select team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                            FROM teams team
                                            WHERE name = "{selected_team}"
                                                AND yearID = {year};''',sqlite_con)
    # roster of pithcers with stats
    player_stats = pd.read_sql_query(f'''SELECT pitcher.yearID, player.nameFirst || ' ' || player.nameLast AS playerName,
                                            round(CAST(pitcher.SO as FLOAT) / (pitcher.BB),2) AS KBB,
                                            IFNULL(pitcher.ERA,0) as ERA
                                        FROM pitching pitcher
                                            JOIN people player ON player.playerID = pitcher.playerID
                                        WHERE pitcher.teamID = "{select_team_id['teamID'][0]}"
                                            AND pitcher.yearID = {year};''',sqlite_con)
    sqlite_con.close()
    # sort roster by ERA
    player_stats = player_stats.sort_values(['ERA'],ascending=True)
    # fill and replace as needed
    player_stats.fillna(0.0, inplace=True)
    player_stats.replace({None: 0.0, '': 0.0}, inplace=True)
    # Create line chart
    era_fig = go.Figure()
    # K/BB ratio with ERA used for bubble size
    era_fig.add_trace(go.Scatter(
        x=player_stats.playerName,
        y=player_stats.KBB,
        mode='markers',
        marker=dict(symbol="circle", size=player_stats.ERA, sizemode='area', 
            sizeref=(2.*max(player_stats.ERA)/(40.**2)), color=player_stats.ERA,
            showscale=True, reversescale=True, colorscale = 'Sunsetdark',
            colorbar=dict(title="ERA")),
        hovertemplate = 'KBB: %{y:.2f}<extra></extra><br>' + '%{text}',
        text = ['ERA: {}'.format(i) for i in player_stats.ERA]))
    # graph options
    era_fig.update_xaxes(title='Pitcher Roster',tickangle=55)
    era_fig.update_yaxes(title='K/BB Ratio')
    era_fig.update_layout(height=600,hovermode="x unified",title="Strikeout-to-Walk Ratio with ERA Bubble",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    # return figure
    return era_fig


# Callback to Line Graph, takes data request from dropdown
@app.callback(
    Output('player-batting-line', 'figure'),
    [Input('era-dropdown', 'value'), Input('league-select-dropdown', 'value'),
    Input('year-select-dropdown', 'value'),Input('player-dropdown', 'value')])
def update_batting_career(selected_era, league, year, selected_player):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # player stats
    player_batting = pd.read_sql_query(f'''SELECT batter.yearID, batter.teamID,
                                            round((CAST(batter.H as FLOAT) - batter.HR) / (batter.AB - IFNULL(batter.SO,0) - batter.HR + IFNULL(batter.SF,0)), 3) as BABIP,
                                            round((CAST(batter.H as FLOAT) + batter.BB + IFNULL(batter.HBP,0)) / (batter.AB + batter.BB + IFNULL(batter.HBP,0) + IFNULL(batter.SF,0)), 3) as OBP,
                                            round(((CAST(batter.H as FLOAT) - batter."2B" - batter."3B" - batter.HR) + (batter."2B" * 2) + (batter."3B" * 3) + (batter.HR * 4)) / batter.AB, 3) as SLG
                                        FROM batting batter
                                        WHERE batter.playerID = "{selected_player}" 
                                            AND batter.yearID >= {year_range[0]} 
                                            AND batter.yearID <= {year_range[1]}
                                        ORDER BY batter.yearID ASC;''',sqlite_con)
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, team.lgID,
                                        round((CAST(team.H as FLOAT) - team.HR) / (team.AB - IFNULL(team.SO,0) - team.HR + IFNULL(team.SF,0)), 3) as BABIP,
                                        round((CAST(team.H as FLOAT) + team.BB + IFNULL(team.HBP,0)) / (team.AB + team.BB + IFNULL(team.HBP,0) + IFNULL(team.SF,0)), 3) as OBP,
                                        round(((CAST(team.H as FLOAT) - team."2B" - team."3B" - team.HR) + (team."2B" * 2) + (team."3B" * 3) + (team.HR * 4)) / team.AB, 3) as SLG
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # fill and replace
    player_batting.fillna(0.0, inplace=True)
    player_batting.replace({None: 0.0, '': 0.0}, inplace=True)
    
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["BABIP", "OBP", "SLG"], index="yearID")
    league_pivot.reset_index(inplace=True)

    # Create Line char figure using Slugging Average, BABIP, and Batting Average
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(name='League SLG', x=league_pivot.yearID, y=league_pivot.SLG, hovertemplate = 'LgSLG: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Orange',opacity=0.6,line = dict( width=3, dash='dot')))
    fig1.add_trace(go.Scatter(name='League OBP', x=league_pivot.yearID, y=league_pivot.OBP, hovertemplate = 'LgOBP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Green',opacity=0.6,line = dict( width=3, dash='dot')))
    fig1.add_trace(go.Scatter(name='League BABIP', x=league_pivot.yearID, y=league_pivot.BABIP, hovertemplate = 'LgBABIP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Gray',opacity=0.6,line = dict( width=3, dash='dot')))

    # prevent pandas warnings
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        # The issue lays with the group by, when it gets only one, future warning occurs
        for team, batting_team in player_batting.groupby(['teamID'], as_index=False):
            fig1.add_trace(go.Scatter(name=team+' Slugging Average', x=batting_team.yearID, y=batting_team.SLG, connectgaps=False, hovertemplate = 'SLG: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#EFB21E',opacity=0.8,line = dict( width=4, dash='dashdot')))
            fig1.add_trace(go.Scatter(name=team+' On-Base Percentage', x=batting_team.yearID, y=batting_team.OBP,  connectgaps=False, hovertemplate = 'OBP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#003831',opacity=0.8,line = dict( width=4, dash='dash')))
            fig1.add_trace(go.Scatter(name=team+' Batting Average Balls In Play', x=batting_team.yearID, y=batting_team.BABIP, connectgaps=False, hovertemplate = 'BABIP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#A2AAAD',opacity=0.8,line = dict(width=3)))

    # set graph options
    fig1.add_vline(x=year, line_width=2.5, line_dash="solid", line_color="Black",opacity=0.25)
    fig1.update_xaxes(title='Year',tickformat='d')
    fig1.update_yaxes(fixedrange=True)
    fig1.update_layout(title="Player Batting Performance for Era",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    fig1.update_layout(hovermode="x", height=550)
    # return figure
    return fig1


# Callback to players batting datatable
@app.callback(
    [Output('player-batting-tabel', 'children')],
    [Input('league-select-dropdown', 'value'),
    Input('player-dropdown', 'value'),Input('year-select-dropdown', 'value')])
def update_batter_table(league, player, year):
    # sql connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, team.lgID,
                                        round((CAST(team.H as FLOAT) - team.HR) / (team.AB - IFNULL(team.SO,0) - team.HR + IFNULL(team.SF,0)), 3) as BABIP,
                                        round((CAST(team.H as FLOAT) + team.BB + IFNULL(team.HBP,0)) / (team.AB + team.BB + IFNULL(team.HBP,0) + IFNULL(team.SF,0)), 3) as OBP,
                                        round(((CAST(team.H as FLOAT) - team."2B" - team."3B" - team.HR) + (team."2B" * 2) + (team."3B" * 3) + (team.HR * 4)) / team.AB, 3) as SLG
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID = {year};''',sqlite_con)
    # player stats
    player_career = pd.read_sql_query(f'''SELECT batter.yearID, batter.teamID, batter.lgID, batter.G,
                                    batter.AB + batter.BB + IFNULL(batter.HBP,0) + IFNULL(batter.SH,0) + IFNULL(batter.SF,0) as PA,
                                    round((CAST(batter.H as FLOAT) - batter.HR) / (batter.AB - batter.SO - batter.HR + IFNULL(batter.SF,0)),3) as BABIP,
                                    round((CAST(batter.H as FLOAT) + batter.BB + IFNULL(batter.HBP,0)) / (batter.AB + batter.BB + IFNULL(batter.HBP,0) + IFNULL(batter.SF,0)),3) as OBP,
                                    round(((CAST(batter.H as FLOAT) - batter."2B" - batter."3B" - batter.HR) + (batter."2B" * 2) + (batter."3B" * 3) + (batter.HR * 4)) / batter.AB,3) as SLG
                                    FROM batting batter
                                    WHERE batter.playerID = "{player}"
                                        AND batter.yearID = {year}
                                    ORDER BY batter.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # pivot table for league data
    league_pivot = pd.pivot_table(league_avg, values=["BABIP","OBP","SLG"], index="yearID")
    league_pivot.reset_index(inplace=True)
    # Fill and replace
    player_career['BABIP'].fillna(format(0,'.3f'),inplace=True)
    player_career['OBP'].fillna(format(0,'.3f'),inplace=True)
    player_career['SLG'].fillna(format(0,'.3f'),inplace=True)
    player_career.replace({None: 0.0, '': 0.0}, inplace=True)
    # Set empty list
    data_note = []
    # if data filter is empty, append and return notice
    if player_career.empty:
        data_note.append(html.Div(dbc.Alert('No Player Batting data is available.', color='warning'),))
        return data_note
    # else set and return datatable
    else:
        data_note.append(html.Div(dash_table.DataTable(
            data= player_career.to_dict('records'),
            columns= [{'name': x, 'id': x} for x in player_career],
            style_as_list_view=True,
            editable=False,
            style_table={
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{{BABIP}} > {}'.format(league_pivot.BABIP[0]),
                        'column_id': 'BABIP'
                    },
                    'backgroundColor': 'darkgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{OBP}} > {}'.format(league_pivot.OBP[0]),
                        'column_id': 'OBP'
                    },
                    'backgroundColor': 'darkgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{SLG}} > {}'.format(league_pivot.SLG[0]),
                        'column_id': 'SLG'
                    },
                    'backgroundColor': 'darkgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{BABIP}} = {}'.format(league_pivot.BABIP[0]),
                        'column_id': 'BABIP'
                    },
                    'backgroundColor': 'gold',
                    'color': 'grey'
                },
                {
                    'if': {
                        'filter_query': '{{OBP}} = {}'.format(league_pivot.OBP[0]),
                        'column_id': 'OBP'
                    },
                    'backgroundColor': 'gold',
                    'color': 'grey'
                },
                {
                    'if': {
                        'filter_query': '{{SLG}} = {}'.format(league_pivot.SLG[0]),
                        'column_id': 'SLG'
                    },
                    'backgroundColor': 'gold',
                    'color': 'grey'
                },
                {
                    'if': {
                        'filter_query': '{{BABIP}} < {}'.format(league_pivot.BABIP[0]),
                        'column_id': 'BABIP'
                    },
                    'backgroundColor': 'darkred',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{OBP}} < {}'.format(league_pivot.OBP[0]),
                        'column_id': 'OBP'
                    },
                    'backgroundColor': 'darkred',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{SLG}} < {}'.format(league_pivot.SLG[0]),
                        'column_id': 'SLG'
                    },
                    'backgroundColor': 'darkred',
                    'color': 'white'
                }]
        ),))
        return data_note


# Callback to Line Chart, Takes request data from dropdown menu
@app.callback(
    Output('player-fielding-line', 'figure'),
    [Input('era-dropdown', 'value'), Input('league-select-dropdown', 'value'),
    Input('year-select-dropdown', 'value'),Input('player-dropdown', 'value'),
    Input('pos-dropdown', 'value')], cache_by=False)
def update_field_career(selected_era, league, year, selected_player, pos):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql query and connect
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # fielding stats
    player_feilding = pd.read_sql_query(f'''SELECT fielder.yearID, fielder.teamID,
                                            round(((CAST(fielder.PO as FLOAT)+fielder.A)/(fielder.PO+fielder.A+fielder.E)),3) as FP
                                            FROM fielding fielder
                                            WHERE fielder.playerID = "{selected_player}"
                                                AND fielder.pos = '{pos}'
                                                AND fielder.yearID >= {year_range[0]} 
                                                AND fielder.yearID <= {year_range[1]}
                                            ORDER BY fielder.yearID ASC;''',sqlite_con)
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, team.FP
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # fill and replace
    player_feilding.fillna(0.0, inplace=True)
    player_feilding.replace({None: 0.0, '': 0.0}, inplace=True)
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["FP"], index="yearID")
    league_pivot["FP"] = league_pivot["FP"].round(3)
    league_pivot.reset_index(inplace=True)
    # Set figure
    fig2 = go.Figure()
    # league
    fig2.add_trace(go.Scatter(name="Lg FPCT", x=league_pivot.yearID, y=league_pivot.FP, hovertemplate = 'LgFPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='grey',opacity=0.8,line = dict(width=4, dash='dashdot')))
    # prevent pandas warnings
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        for team, player_team in player_feilding.groupby(['teamID'], as_index=False):
            fig2.add_trace(go.Scatter(name=team+" FPCT", x=player_team[player_team.teamID == team].yearID, y=player_team[player_team.teamID == team].FP, hovertemplate = 'Player FPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='rebeccapurple',opacity=0.6,line = dict(width=4)))
    # update figure
    fig2.add_vline(x=year, line_width=2.5, line_dash="solid", line_color="Black",opacity=0.25)
    fig2.update_xaxes(title='Year',tickformat='d')
    fig2.update_yaxes(fixedrange=True)
    fig2.update_layout(hovermode="x",title="Team Fielding Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig2


# fielding datatable
@app.callback(
    [Output('player-field-tabel', 'children')],
    [Input('player-dropdown', 'value'),Input('year-select-dropdown', 'value'),
    Input('era-dropdown', 'value'),Input('league-select-dropdown', 'value'),
    Input('pos-dropdown', 'value')])
def update_field_table(player, year, selected_era, league, pos):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # player stats
    player_career = pd.read_sql_query(f'''SELECT fielder.yearID, fielder.teamID, fielder.lgID, fielder.POS, fielder.G,
                                            fielder.PO, fielder.A, fielder.E, fielder.DP, round(((CAST(fielder.PO as FLOAT)+fielder.A)/(fielder.PO+fielder.A+fielder.E)),3) as FP
                                FROM fielding fielder
                                WHERE fielder.playerID = '{player}'
                                    AND fielder.yearID = {year}
                                    AND fielder.pos = '{pos}'
                                ORDER BY fielder.yearID ASC;''',sqlite_con)
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, team.FP
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # fill and replace
    player_career.fillna(0.0, inplace=True)
    player_career.replace({None: 0.0, '': 0.0}, inplace=True)
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["FP"], index="yearID")
    league_pivot["FP"] = league_pivot["FP"].round(3)
    league_pivot.reset_index(inplace=True)
    # Set empty list
    data_note = []
    # if data filter is empty, append and return notice
    if player_career.empty:
        data_note.append(html.Div(dbc.Alert('No Player Fielding data is available.', color='warning'),))
        return data_note
    # else set and return datatable
    else:
        data_note.append(html.Div(dash_table.DataTable(
            data= player_career.to_dict('records'),
            columns= [{'name': x, 'id': x} for x in player_career],
            style_as_list_view=True,
            editable=False,
            style_table={
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{{FP}} > {}'.format(league_pivot.FP[0]),
                        'column_id': 'FP'
                    },
                    'backgroundColor': 'darkgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{FP}} = {}'.format(league_pivot.FP[0]),
                        'column_id': 'FP'
                    },
                    'backgroundColor': 'gold',
                    'color': 'grey'
                },
                {
                    'if': {
                        'filter_query': '{{FP}} < {}'.format(league_pivot.FP[0]),
                        'column_id': 'FP'
                    },
                    'backgroundColor': 'darkred',
                    'color': 'white'
                }]
        ),))
        return data_note


# Callback to pitching graph
@app.callback(
    Output('player-pitching-graph', 'children'),
    [Input('era-dropdown', 'value'), Input('league-select-dropdown', 'value'),
    Input('year-select-dropdown', 'value'),Input('player-dropdown', 'value')])
def update_pitch_career(selected_era, league, year, selected_player):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # pitching stats
    pitching_career = pd.read_sql_query(f'''SELECT pitcher.yearID, round(CAST(pitcher.SO as FLOAT)/pitcher.BB,2) as KBB,
                                                pitcher.ERA
                                            FROM pitching pitcher
                                            WHERE pitcher.playerID = "{selected_player}" 
                                                AND pitcher.yearID >= {year_range[0]} 
                                                AND pitcher.yearID <= {year_range[1]}
                                            ORDER BY pitcher.yearID ASC;''',sqlite_con)
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, round(CAST(team.SOA as FLOAT)/team.BBA,2) as KBB, team.ERA
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # if career is empty, negate league data with empty dataframe
    if pitching_career.empty:
        del league_avg
        league_pivot = pd.DataFrame()
    else:
        # fill and replace
        pitching_career.fillna(0.0, inplace=True)
        pitching_career.replace({None: 0.0, '': 0.0}, inplace=True)
        # league pivot table
        league_pivot = pd.pivot_table(league_avg, values=["KBB","ERA"], index="yearID")
        league_pivot['ERA'] = league_pivot['ERA'].round(2)
        league_pivot['KBB'] = league_pivot['KBB'].round(2)
        league_pivot.reset_index(inplace=True)
    # set graphing figure
    fig3 = go.Figure()
    # if league data is not empty
    if league_pivot.empty == False:
        fig3.add_trace(go.Scatter(
            name="League",
            x=league_pivot.yearID,
            y=league_pivot.KBB,
            mode='markers',
            marker=dict(symbol="circle", size=league_pivot.ERA, sizemode='area', 
                sizeref=(2.*max(league_pivot.ERA)/(40.**2)), color=league_pivot.ERA,
                showscale=True, reversescale=True, colorscale = 'Tealgrn',
                colorbar=dict(title="LgERA",x=1.1)),
            hovertemplate = 'LgKBB: %{y:.2f}<extra></extra><br>' + '%{text}',
            text = ['LgERA: {}'.format(i) for i in league_pivot.ERA]))
    # if player data is not empty
    if pitching_career.empty == False:
        fig3.add_trace(go.Scatter(
            name="Player",
            x=pitching_career.yearID,
            y=pitching_career.KBB,
            mode='markers',
            marker=dict(symbol="circle", size=pitching_career.ERA, sizemode='area', 
                sizeref=(2.*max(pitching_career.ERA)/(40.**2)), color=pitching_career.ERA,
                showscale=True, reversescale=True, colorscale = 'Sunsetdark',
                colorbar=dict(title="ERA")),
            hovertemplate = 'KBB: %{y:.2f}<extra></extra><br>' + '%{text}',
            text = ['ERA: {}'.format(i) for i in pitching_career.ERA]))
        # update options
        fig3.add_vline(x=year, line_width=2.5, line_dash="solid", line_color="Black", opacity=0.25)
        fig3.update_yaxes(title='K/BB Ratio', tickformat='d')
        fig3.update_layout(height=600,title="Player Strikeout-to-Walk Ratio with ERA",
            font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
        fig3.update_layout(legend=dict(orientation="h",
            yanchor="bottom",y=1.02,xanchor="right",x=1))
    # if player stats are not empty
    if pitching_career.empty == False:
        graph = dcc.Graph(figure=fig3, config={'displayModeBar': False})
    else:
        graph = html.P()
    # return graph
    return graph


# pitchers datatable
@app.callback(
    [Output('player-pitch-tabel', 'children')],
    [Input('player-dropdown', 'value'),Input('year-select-dropdown', 'value'),
    Input('era-dropdown', 'value'),Input('league-select-dropdown', 'value')])
def update_pitch_table(player, year, selected_era, league):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # player stats
    player_career = pd.read_sql_query(f'''SELECT pitcher.yearID, pitcher.teamID, pitcher.lgID, pitcher.W, pitcher.L,
                                            pitcher.G, pitcher.BAOpp, round(CAST(pitcher.SO as FLOAT)/pitcher.BB,2) AS KBB, pitcher.ERA
                                FROM pitching pitcher
                                WHERE pitcher.playerID = '{player}'
                                    AND pitcher.yearID = {year}
                                ORDER BY pitcher.yearID ASC;''',sqlite_con)
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, round(CAST(team.SOA as FLOAT)/team.BBA,2) as KBB, team.ERA
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # fill and replace
    player_career.fillna(0.0, inplace=True)
    player_career.replace({None: 0.0, '': 0.0}, inplace=True)
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["KBB","ERA"], index="yearID")
    league_pivot['ERA'] = league_pivot['ERA'].round(2)
    league_pivot['KBB'] = league_pivot['KBB'].round(2)
    league_pivot.reset_index(inplace=True)
    # Set empty list
    data_note = []
    # if data filter is empty, append and return notice
    if player_career.empty:
        data_note.append(html.Div(dbc.Alert('No Player Pitching data is available.', color='warning')))
        return data_note
    # else set and return datatable
    else:
        data_note.append(html.Div(dash_table.DataTable(
            data= player_career.to_dict('records'),
            columns= [{'name': x, 'id': x} for x in player_career],
            style_as_list_view=True,
            editable=False,
            style_table={
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{{KBB}} > {}'.format(league_pivot.KBB[0]),
                        'column_id': 'KBB'
                    },
                    'backgroundColor': 'darkgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{ERA}} < {}'.format(league_pivot.ERA[0]),
                        'column_id': 'ERA'
                    },
                    'backgroundColor': 'darkgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{KBB}} = {}'.format(league_pivot.KBB[0]),
                        'column_id': 'KBB'
                    },
                    'backgroundColor': 'gold',
                    'color': 'grey'
                },
                {
                    'if': {
                        'filter_query': '{{ERA}} = {}'.format(league_pivot.ERA[0]),
                        'column_id': 'ERA'
                    },
                    'backgroundColor': 'gold',
                    'color': 'grey'
                },
                {
                    'if': {
                        'filter_query': '{{KBB}} < {}'.format(league_pivot.KBB[0]),
                        'column_id': 'KBB'
                    },
                    'backgroundColor': 'darkred',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{{ERA}} > {}'.format(league_pivot.ERA[0]),
                        'column_id': 'ERA'
                    },
                    'backgroundColor': 'darkred',
                    'color': 'white'
                }]
        ),))
        return data_note