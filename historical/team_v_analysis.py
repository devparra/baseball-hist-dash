# import dash IO and graph objects
from dash.dependencies import Input, Output
# Plotly graph objects to render graph plots
import plotly.graph_objects as go

# Import app
from app import app

# Pandas and SQLite3
from data.data import pd, sl, np
# Custom functions
from data.data import dynamicteams, dynamicrange, dynamicleagues


# This will update the league dropdowns
@app.callback(
    [Output('league-one-dropdown', 'options'),Output('league-one-dropdown', 'value')],
    [Output('league-two-dropdown', 'options'),Output('league-two-dropdown', 'value')],
    [Input('era-dropdown', 'value')])
def select_league_era(selected_era):
    # Select era and generate leagues list
    leagues = dynamicleagues(selected_era)
    # Return league list
    return leagues, leagues[0]['value'], leagues, leagues[1]['value']


# This will update the team A dropdown
@app.callback(
    [Output('team-one-dropdown', 'options'),Output('team-one-dropdown', 'value')],
    [Input('era-dropdown', 'value'),Input('league-one-dropdown', 'value')])
def select_team_one(selected_era, selected_league):
    # select era and league, generate teams list
    teams = dynamicteams(selected_era, selected_league)
    # Return team list A
    return teams, teams[0]['value']


# This will update the team B dropdown
@app.callback(
    [Output('team-two-dropdown', 'options'),Output('team-two-dropdown', 'value')],
    [Input('era-dropdown', 'value'),Input('league-two-dropdown', 'value')])
def select_team_two(selected_era,selected_league):
    # select era and league, generate teams list
    teams = dynamicteams(selected_era,selected_league)
    # Return team list B
    return teams, teams[1]['value']


# team A park info
@app.callback(
    [Output('team-one-table', 'data'),Output('team-one-table','columns')],
    [Input('team-one-dropdown', 'value'),Input('era-dropdown', 'value')])
def team_one_table(selected_team, selected_era):
    # select era range
    year_range = dynamicrange(selected_era)
    # sql connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    team_one_query = pd.read_sql_query(f'''SELECT yearID, lgID, IFNULL(team.divID, "-") as Div, IFNULL(park, "-") as park, 
                                        IFNULL(FLOOR(attendance / Ghome), 0) as avgAtt, IFNULL(BPF, 0) as ParkFactor
                                            FROM teams team
                                        WHERE name = "{selected_team}"
                                        AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # Create a pivot table for parks
    team_one_pivot = pd.pivot_table(team_one_query, index=['park'], values=['ParkFactor', 'avgAtt'])
    team_one_pivot.reset_index(inplace=True)
    # set average attendence, lowest
    team_one_pivot['avgAtt'] = team_one_pivot['avgAtt'].apply(np.floor)
    # set park factor, round number
    team_one_pivot['ParkFactor'] = team_one_pivot['ParkFactor'].apply(np.round)
    team_one_pivot.rename(columns={"ParkFactor":"AvgParkFactor", "avgAtt": "CombAvgAtt"},inplace=True)
    # Return park data, team A
    return team_one_pivot.to_dict('records'), [{'name': x, 'id': x} for x in team_one_pivot]


# team B park info
@app.callback(
    [Output('team-two-table', 'data'),Output('team-two-table','columns')],
    [Input('team-two-dropdown', 'value'),Input('era-dropdown', 'value')])
def team_two_table(selected_team, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    team_two_query = pd.read_sql_query(f'''SELECT yearID, lgID, IFNULL(team.divID, "-") as Div, IFNULL(park, "-") as park, 
                                        IFNULL(FLOOR(attendance / Ghome),0) as avgAtt, IFNULL(BPF, 0) as ParkFactor
                                        FROM teams team
                                    WHERE name = "{selected_team}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # set pivot table for team B park(s)
    team_two_pivot = pd.pivot_table(team_two_query, index=['park'], values=['ParkFactor', 'avgAtt'])
    team_two_pivot.reset_index(inplace=True)
    # set average attendence, low
    team_two_pivot['avgAtt'] = team_two_pivot['avgAtt'].apply(np.floor)
    # set park factor
    team_two_pivot['ParkFactor'] = team_two_pivot['ParkFactor'].apply(np.round)
    team_two_pivot.rename(columns={"ParkFactor":"AvgParkFactor", "avgAtt": "CombAvgAtt"},inplace=True)
    # Return park data for team B
    return team_two_pivot.to_dict('records'), [{'name': x, 'id': x} for x in team_two_pivot]


# team A champ info
@app.callback(
    [Output('team-one-champ', 'data'),Output('team-one-champ','columns')],
    [Input('team-one-dropdown', 'value'),Input('era-dropdown', 'value')])
def team_one_champ(selected_team, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    team_one_query = pd.read_sql_query(f'''SELECT yearID, teamID, lgID, IFNULL(team.divID, "-") as Div, IFNULL(team.DivWin,"-") as DivTitle, IFNULL(team.WCWin,"-") as WildCard, 
                                        IFNULL(team.LgWin,"-") as LgChamp, IFNULL(team.WSWin,"-") as WSChamp
                                        FROM teams team
                                    WHERE name = "{selected_team}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # Replace values in dataframe
    team_one_query.replace({'DivTitle': {'Y': True, 'N': False, '-': False}, 'WildCard': {'Y': True, 'N': False, '-': False}, 
                    'LgChamp': {'Y': True, 'N': False, '-': False}, 'WSChamp': {'Y': True, 'N': False, '-': False}},inplace=True)
    # create a pivot table for team A titles
    team_one_pivot = pd.pivot_table(team_one_query, index="teamID", values=['DivTitle','WildCard', 'LgChamp', 'WSChamp'], aggfunc="sum")
    team_one_pivot.reset_index(inplace=True)
    # Return team A champ data
    return team_one_pivot.to_dict('records'), [{'name': x, 'id': x} for x in team_one_pivot]


# team B champ info
@app.callback(
    [Output('team-two-champ', 'data'),Output('team-two-champ','columns')],
    [Input('team-two-dropdown', 'value'),Input('era-dropdown', 'value')])
def team_two_champ(selected_team, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    team_two_query = pd.read_sql_query(f'''SELECT yearID, teamID, lgID, IFNULL(team.divID, "-") as Div, IFNULL(team.DivWin,"-") as DivTitle, IFNULL(team.WCWin,"-") as WildCard, 
                                        IFNULL(team.LgWin,"-") as LgChamp, IFNULL(team.WSWin,"-") as WSChamp
                                        FROM teams team
                                    WHERE name = "{selected_team}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # replace value in dataframe
    team_two_query.replace({'DivTitle': {'Y': True, 'N': False, '-': False}, 'WildCard': {'Y': True, 'N': False, '-': False}, 
                    'LgChamp': {'Y': True, 'N': False, '-': False}, 'WSChamp': {'Y': True, 'N': False, '-': False}},inplace=True)
    # team b pivot table
    team_two_pivot = pd.pivot_table(team_two_query, index="teamID", values=['DivTitle','WildCard', 'LgChamp', 'WSChamp'], aggfunc="sum")
    team_two_pivot.reset_index(inplace=True)
    # Return team B champ data
    return team_two_pivot.to_dict('records'), [{'name': x, 'id': x} for x in team_two_pivot]


# Compare team WL callback
@app.callback(
    Output('teamv-wl-line', 'figure'),
    [Input('team-one-dropdown', 'value'),Input('team-two-dropdown', 'value'),Input('era-dropdown', 'value')])
def update_figure1(selected_team_a, selected_team_b, selected_era):
    # select era
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team A
    team_a_winloss = pd.read_sql_query(f'''SELECT team.yearID, team.name, round(cast(team.W as FLOAT) / (team.W + team.L), 3) as wPCT
                                FROM teams team
                                WHERE team.name = "{selected_team_a}"
                                    AND team.yearID >= {year_range[0]} 
                                    AND team.yearID <= {year_range[1]}
                                ORDER BY team.yearID ASC;''',sqlite_con)
    # Team B
    team_b_winloss = pd.read_sql_query(f'''SELECT team.yearID, team.name, round(cast(team.W as FLOAT) / (team.W + team.L), 3) as wPCT
                                FROM teams team
                                WHERE team.name = "{selected_team_b}"
                                    AND team.yearID >= {year_range[0]} 
                                    AND team.yearID <= {year_range[1]}
                                ORDER BY team.yearID ASC;''',sqlite_con)
    sqlite_con.close()

    # Create Bar Chart figure, Wins and Losses
    fig1 = go.Figure(data=[
        go.Scatter(name=team_a_winloss.name[0] + " wPCT", x=team_a_winloss.yearID, y=team_a_winloss.wPCT, hovertemplate = team_a_winloss.name[0] + ' wPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#004687',opacity=0.8,line = dict( width=4)),
        go.Scatter(name=team_b_winloss.name[0]  + " wPCT", x=team_b_winloss.yearID, y=team_b_winloss.wPCT, hovertemplate = team_b_winloss.name[0] +  ' wPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#BD9B60',opacity=0.8,line = dict( width=4, dash='dashdot')),
    ])
    # set options
    fig1.update_xaxes(title='Year',tickformat='d')
    fig1.update_yaxes(fixedrange=True)
    fig1.update_layout(hovermode="x",barmode='group',title="Team v Team Win/Loss Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig1


# compare team batting callback
@app.callback(
    Output('teamv-batting-line', 'figure'),
    [Input('team-one-dropdown', 'value'),Input('team-two-dropdown', 'value'),
    Input('era-dropdown', 'value')])
def update_figure2(selected_team_a, selected_team_b, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team A
    team_a_batting = pd.read_sql_query(f'''SELECT team.yearID, team.Name,
                        round((CAST(team.H as FLOAT)) / team.AB, 3) as BA,
                        round((CAST(team.H as FLOAT) + team.BB + IFNULL(team.HBP,0)) / (team.AB + team.BB + IFNULL(team.HBP,0) + IFNULL(team.SF,0)), 3) as OBP,
                        round(((CAST(team.H as FLOAT) - team."2B" - team."3B" - team.HR) + (team."2B" * 2) + (team."3B" * 3) + (team.HR * 4)) / team.AB, 3) as SLG
                    FROM teams team
                    WHERE team.name = "{selected_team_a}"
                        AND team.yearID >= {year_range[0]} 
                        AND team.yearID <= {year_range[1]}
                    ORDER BY team.yearID ASC;''',sqlite_con)
    # Team B
    team_b_batting = pd.read_sql_query(f'''SELECT team.yearID, team.Name,
                        round((CAST(team.H as FLOAT)) / team.AB, 3) as BA,
                        round((CAST(team.H as FLOAT) + team.BB + IFNULL(team.HBP,0)) / (team.AB + team.BB + IFNULL(team.HBP,0) + IFNULL(team.SF,0)), 3) as OBP,
                        round(((CAST(team.H as FLOAT) - team."2B" - team."3B" - team.HR) + (team."2B" * 2) + (team."3B" * 3) + (team.HR * 4)) / team.AB, 3) as SLG
                    FROM teams team
                    WHERE team.name = "{selected_team_b}"
                        AND team.yearID >= {year_range[0]} 
                        AND team.yearID <= {year_range[1]}
                    ORDER BY team.yearID ASC;''',sqlite_con)
    sqlite_con.close()

    # Line graph of batting stats
    fig2 = go.Figure(data=[
        go.Scatter(name=team_a_batting.name[0] + " BA", x=team_a_batting.yearID, y=team_a_batting.BA, hovertemplate = team_a_batting.name[0] + ' BA: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Green',opacity=0.8,line = dict( width=4)),
        go.Scatter(name=team_b_batting.name[0] + " BA", x=team_b_batting.yearID, y=team_b_batting.BA, hovertemplate = team_b_batting.name[0] + ' BA: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#003831',opacity=0.8,line = dict( width=4, dash='dashdot')),
        go.Scatter(name=team_a_batting.name[0] + " OBP", x=team_a_batting.yearID, y=team_a_batting.OBP, hovertemplate = team_a_batting.name[0] + ' OBP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Orange',opacity=0.8,line = dict( width=4)),
        go.Scatter(name=team_b_batting.name[0] + " OBP", x=team_b_batting.yearID, y=team_b_batting.OBP, hovertemplate = team_b_batting.name[0] + ' OBP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#EFB21E',opacity=0.8,line = dict( width=4, dash='dashdot')),
        go.Scatter(name=team_a_batting.name[0] + " SLG", x=team_a_batting.yearID, y=team_a_batting.SLG, hovertemplate = team_a_batting.name[0] + ' SLG: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Grey',opacity=0.8,line = dict( width=4)),
        go.Scatter(name=team_b_batting.name[0] + " SLG", x=team_b_batting.yearID, y=team_b_batting.SLG, hovertemplate = team_b_batting.name[0] + ' SLG: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#A2AAAD',opacity=0.8,line = dict( width=4, dash='dashdot')),
    ])
    # set graph options
    fig2.update_xaxes(title='Year',tickformat='d')
    fig2.update_yaxes(fixedrange=True)
    fig2.update_layout(hovermode="x", title="Team v Team Batting Performance",
        font={'color':'darkslategray'}, paper_bgcolor='white', plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig2


# compare team pitching callback
@app.callback(
    Output('teamv-pitch-line', 'figure'),
    [Input('team-one-dropdown', 'value'),Input('team-two-dropdown', 'value'),
    Input('era-dropdown', 'value')])
def update_figure3(selected_team_a, selected_team_b, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team A
    team_a_pitching = pd.read_sql_query(f'''SELECT team.yearID, team.Name, team.ERA
                    FROM teams team
                    WHERE team.name = "{selected_team_a}"
                        AND team.yearID >= {year_range[0]} 
                        AND team.yearID <= {year_range[1]}
                    ORDER BY team.yearID ASC;''',sqlite_con)
    # team B
    team_b_pitching = pd.read_sql_query(f'''SELECT team.yearID, team.Name, team.ERA
                    FROM teams team
                    WHERE team.name = "{selected_team_b}"
                        AND team.yearID >= {year_range[0]} 
                        AND team.yearID <= {year_range[1]}
                    ORDER BY team.yearID ASC;''',sqlite_con)
    sqlite_con.close()

    # Create line graph of team Earned Runs Avgerage
    fig3 = go.Figure(data=[
        go.Scatter(name=team_a_pitching.name[0] + " ERA", x=team_a_pitching.yearID, y=team_a_pitching.ERA, hovertemplate = team_a_pitching.name[0] + ' ERA: %{y:.2f}<extra></extra><br>', mode='lines+markers', marker_color='#002B5C',opacity=0.8,line = dict( width=4)),
        go.Scatter(name=team_b_pitching.name[0] + " ERA", x=team_b_pitching.yearID, y=team_b_pitching.ERA, hovertemplate = team_b_pitching.name[0] + ' ERA: %{y:.2f}<extra></extra><br>', mode='lines+markers', marker_color='#D31145',opacity=0.8,line = dict( width=4, dash='dashdot')),
    ])
    # set graph options
    fig3.update_xaxes(title='Year',tickformat='d')
    fig3.update_yaxes(fixedrange=True)
    fig3.update_layout(hovermode="x", title="Team v Team Pitching Performance",
        font={'color':'darkslategray'}, paper_bgcolor='white', plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig3


# compare team fielding callback
@app.callback(
    Output('teamv-field-line', 'figure'),
    [Input('team-one-dropdown', 'value'),Input('team-two-dropdown', 'value'),
    Input('era-dropdown', 'value')])
def update_figure4(selected_team_a, selected_team_b, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team A
    team_a_feilding = pd.read_sql_query(f'''SELECT team.yearID, team.Name, team.FP
                    FROM teams team
                    WHERE team.name = "{selected_team_a}"
                        AND team.yearID >= {year_range[0]} 
                        AND team.yearID <= {year_range[1]}
                    ORDER BY team.yearID ASC;''',sqlite_con)
    # team B
    team_b_feilding = pd.read_sql_query(f'''SELECT team.yearID, team.Name, team.FP
                    FROM teams team
                    WHERE team.name = "{selected_team_b}"
                        AND team.yearID >= {year_range[0]} 
                        AND team.yearID <= {year_range[1]}
                    ORDER BY team.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # graph of feilding percentage
    fig4 = go.Figure(data=[
        go.Scatter(name=team_a_feilding.name[0] + " FPCT", x=team_a_feilding.yearID, y=team_a_feilding.FP, hovertemplate = team_a_feilding.name[0] + ' FPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='rebeccapurple',opacity=0.8,line = dict( width=4)),
        go.Scatter(name=team_b_feilding.name[0] + " FPCT", x=team_b_feilding.yearID, y=team_b_feilding.FP, hovertemplate = team_b_feilding.name[0] + ' FPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='black',opacity=0.4,line = dict( width=4, dash='dashdot')),
    ])
    # set options
    fig4.update_xaxes(title='Year',tickformat='d')
    fig4.update_yaxes(fixedrange=True)
    fig4.update_layout(hovermode="x", title="Team v Team Feilding Performance",
        font={'color':'darkslategray'}, paper_bgcolor='white', plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig4