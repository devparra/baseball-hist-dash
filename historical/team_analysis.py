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


# This will update the team dropdown
@app.callback(
    [Output('league-dropdown', 'options'),
    Output('league-dropdown', 'value')],
    [Input('era-dropdown', 'value')])
def select_league_era(selected_era):
    # select era, generate list of leagues
    leagues = dynamicleagues(selected_era)
    # return league list
    return leagues, leagues[0]['value']


# This will update the team dropdown
@app.callback(
    [Output('team-dropdown', 'options'),
    Output('team-dropdown', 'value')],
    [Input('era-dropdown', 'value'),Input('league-dropdown', 'value')])
def select_team_era(selected_era,selected_league):
    # select era and league
    teams = dynamicteams(selected_era,selected_league)
    # Return team list
    return teams, teams[0]['value']


# team championship data
@app.callback(
    [Output('team-champ', 'data'),Output('team-champ','columns')],
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value')])
def team_champ(selected_team, selected_era):
    # selct year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team data
    team_query = pd.read_sql_query(f'''SELECT yearID, name, lgID, IFNULL(team.divID, "-") as Div, IFNULL(team.DivWin,"-") as DivTitle, IFNULL(team.WCWin,"-") as WildCard, 
                                                IFNULL(team.LgWin,"-") as LgChamp, IFNULL(team.WSWin,"-") as WSChamp
                                            FROM teams team
                                            WHERE name = "{selected_team}" AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # Data replace
    team_query.replace({'DivTitle': {'Y': True, 'N': False, '-': False}, 'WildCard': {'Y': True, 'N': False, '-': False}, 
                    'LgChamp': {'Y': True, 'N': False, '-': False}, 'WSChamp': {'Y': True, 'N': False, '-': False}},inplace=True)
    # Team pivot table
    team_pivot = pd.pivot_table(team_query, index=["name","lgID"], values=['DivTitle','WildCard', 'LgChamp', 'WSChamp'], aggfunc=np.sum)
    team_pivot.reset_index(inplace=True)
    # Return team data
    return team_pivot.to_dict('records'), [{'name': x, 'id': x} for x in team_pivot]


# team post season data
@app.callback(
    [Output('team-post-table', 'data'),Output('team-post-table','columns')],
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value')])
def team_post_data(selected_team, selected_era):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # post season series data
    series_data = pd.read_sql_query(f'''SELECT DISTINCT series.yearID, series.round, 
                                        (SELECT DISTINCT team.name
                                                FROM teams team
                                            WHERE team.teamID = series.teamIDwinner
                                                AND team.yearID >= {year_range[0]} AND team.yearID <= {year_range[1]}) as Winner,
                                        (SELECT DISTINCT team.name
                                                FROM teams team
                                            WHERE team.teamID = series.teamIDloser
                                                AND team.yearID >= {year_range[0]} AND team.yearID <= {year_range[1]}) as Loser, 
                                                wins || " - " || losses  as Record
                                    FROM seriespost series
                                    WHERE series.yearID >= {year_range[0]} AND series.yearID <= {year_range[1]}
                                    ORDER BY series.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # set dataframe
    series_data = series_data[(series_data['Winner'] == selected_team) | (series_data['Loser'] == selected_team)]
    series_data.reset_index(drop=True,inplace=True)
    # Return post season data
    return series_data.to_dict('records'), [{'name': x, 'id': x} for x in series_data]


# Callback Bar Chart
@app.callback(
    Output('wl-bar', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value')])
def update_figure1(selected_team, selected_era):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team data
    team_winloss = pd.read_sql_query(f'''SELECT team.yearID, team.teamID, team.W, team.L
                                FROM teams team
                                WHERE team.name = "{selected_team}"
                                    AND team.yearID >= {year_range[0]} 
                                    AND team.yearID <= {year_range[1]}
                                ORDER BY team.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # Create Bar Chart figure, Wins and Losses
    fig1 = go.Figure(data=[
        go.Bar(name='Wins', x=team_winloss.yearID, y=team_winloss.W, marker_color='#004687',opacity=0.8),
        go.Bar(name='Losses', x=team_winloss.yearID, y=team_winloss.L,  marker_color='#AE8F6F',opacity=0.8)
    ])
    # set graph options
    # set x axes title and tick to only include year given no half year such as 1927.5
    fig1.update_xaxes(title='Year',tickformat='d')
    # set y axes to fixed selection range, user can only select data in the x axes
    fig1.update_yaxes(fixedrange=True)
    # Update figure, set hover to the X-Axis and establish title
    fig1.update_layout(hovermode="x",barmode='group',title="Win/Loss Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig1


# Callback to Line Graph
@app.callback(
    Output('batting-line', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value'), 
    Input('league-dropdown', 'value')])
def update_figure2(selected_team, selected_era , league):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team stats
    team_batting = pd.read_sql_query(f'''SELECT team.yearID,
                                            round((CAST(team.H as FLOAT) - team.HR) / (team.AB - IFNULL(team.SO,0) - team.HR + IFNULL(team.SF,0)), 3) as BABIP,
                                            round((CAST(team.H as FLOAT) + team.BB + IFNULL(team.HBP,0)) / (team.AB + team.BB + IFNULL(team.HBP,0) + IFNULL(team.SF,0)), 3) as OBP,
                                            round(((CAST(team.H as FLOAT) - team."2B" - team."3B" - team.HR) + (team."2B" * 2) + (team."3B" * 3) + (team.HR * 4)) / team.AB, 3) as SLG
                                        FROM teams team
                                        WHERE team.name = "{selected_team}" 
                                            AND team.yearID >= {year_range[0]} 
                                            AND team.yearID <= {year_range[1]}
                                        ORDER BY team.yearID ASC;''',sqlite_con)
    # league stats
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, team.lgID,
                                        round((CAST(team.H as FLOAT) - team.HR) / (team.AB - IFNULL(team.SO,0) - team.HR + IFNULL(team.SF,0)), 3) as BABIP,
                                        round((CAST(team.H as FLOAT) + team.BB + IFNULL(team.HBP,0)) / (team.AB + team.BB + IFNULL(team.HBP,0) + IFNULL(team.SF,0)), 3) as OBP,
                                        round(((CAST(team.H as FLOAT) - team."2B" - team."3B" - team.HR) + (team."2B" * 2) + (team."3B" * 3) + (team.HR * 4)) / team.AB, 3) as SLG
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["BABIP", "OBP", "SLG"], index="yearID")
    league_pivot.reset_index(inplace=True)
    # Create Line char figure using Slugging Average, BABIP, and Batting Average
    fig2 = go.Figure(data=[
        go.Scatter(name='Team SLG', x=team_batting.yearID, y=team_batting.SLG, hovertemplate = 'SLG: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#EFB21E',opacity=0.8,line = dict( width=4, dash='dashdot')),
        go.Scatter(name='League SLG', x=league_pivot.yearID, y=league_pivot.SLG, hovertemplate = 'LgSLG: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Orange',opacity=0.6,line = dict( width=3, dash='dot')),
        go.Scatter(name='Team OBP', x=team_batting.yearID, y=team_batting.OBP, hovertemplate = 'OBP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#003831',opacity=0.8,line = dict( width=4, dash='dash')),        
        go.Scatter(name='League OBP', x=league_pivot.yearID, y=league_pivot.OBP, hovertemplate = 'LgOBP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Green',opacity=0.6,line = dict( width=3, dash='dot')),
        go.Scatter(name='Team BABIP', x=team_batting.yearID, y=team_batting.BABIP, hovertemplate = 'BABIP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='#A2AAAD',opacity=0.8,line = dict(width=3)),
        go.Scatter(name='League BABIP', x=league_pivot.yearID, y=league_pivot.BABIP, hovertemplate = 'LgBABIP: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='Gray',opacity=0.6,line = dict( width=3, dash='dot'))
    ])

    # update graph options
    fig2.update_xaxes(title='Year',tickformat='d')
    fig2.update_yaxes(fixedrange=True)
    fig2.update_layout(title="Team Batting Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    fig2.update_layout(hovermode="x unified")
    # return graph
    return fig2


# Callback to fielding Line Chart
@app.callback(
    Output('feild-line', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value'),
    Input('league-dropdown', 'value')])
def update_figure3(selected_team, selected_era, league):
    # select year range
    year_range = dynamicrange(selected_era)
    # sql query and connection
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team data
    team_feilding = pd.read_sql_query(f'''SELECT team.yearID, team.name, team.FP
                                FROM teams team
                                WHERE team.name = "{selected_team}" 
                                    AND team.yearID >= {year_range[0]} 
                                    AND team.yearID <= {year_range[1]}
                                ORDER BY team.yearID ASC;''',sqlite_con)
    # league data
    league_avg = pd.read_sql_query(f'''SELECT team.yearID, team.lgID, team.FP
                                        FROM teams team
                                    WHERE team.lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["FP"], index="yearID")
    league_pivot["FP"] = league_pivot["FP"].round(3)
    league_pivot.reset_index(inplace=True)

    # Set figure
    fig3 = go.Figure(data=[
        go.Scatter(name="Team FPCT", x=team_feilding.yearID, y=team_feilding.FP, hovertemplate = team_feilding.name[0] + ' FPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='rebeccapurple',opacity=0.8,line = dict( width=4)),
        go.Scatter(name="League FPCT", x=league_pivot.yearID, y=league_pivot.FP, hovertemplate = 'League FPCT: %{y:.3f}<extra></extra><br>', mode='lines+markers', marker_color='black',opacity=0.4,line = dict( width=4, dash='dashdot')),
    ])
    
    # update figure
    fig3.update_xaxes(title='Year',tickformat='d')
    fig3.update_yaxes(fixedrange=True)
    fig3.update_layout(hovermode="x unified",title="Team Fielding Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0',
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # return figure
    return fig3


# Call back to Line Bubble Chart
@app.callback(
    Output('pitch-bubble', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value'), Input('league-dropdown', 'value')])
def update_figure5(selected_team, selected_era, league):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # team data
    team_pitching = pd.read_sql_query(f'''SELECT team.yearID, team.name, team.ERA,
                                                round(CAST(team.SOA as FLOAT) / (team.BBA),2) AS KBB
                                            FROM teams team
                                            WHERE team.name = "{selected_team}" 
                                                AND team.yearID >= {year_range[0]} 
                                                AND team.yearID <= {year_range[1]}
                                            ORDER BY team.yearID ASC;''',sqlite_con)
    # league data
    league_avg = pd.read_sql_query(f'''SELECT yearID, lgID, ERA,
                                            round(CAST(team.SOA as FLOAT) / (team.BBA),2) AS KBB
                                        FROM teams team
                                    WHERE lgID = "{league}"
                                    AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    sqlite_con.close()
    # league pivot table
    league_pivot = pd.pivot_table(league_avg, values=["ERA", "KBB"], index="yearID")
    league_pivot['ERA'] = league_pivot['ERA'].round(2)
    league_pivot['KBB'] = league_pivot['KBB'].round(2)
    league_pivot.reset_index(inplace=True)
    # Create line chart of K/BB ratio with ERA used for bubble size
    fig5 = go.Figure()
    # league
    fig5.add_trace(go.Scatter(
        name="League",
        x=league_pivot.yearID,
        y=league_pivot.KBB,
        mode='markers',
        marker=dict(symbol="circle", size=league_pivot.ERA, sizemode='area', 
            sizeref=(2.*max(league_pivot.ERA)/(40.**2)), color=league_pivot.ERA,
            showscale=True, reversescale=True, colorscale = 'Tealgrn',
            colorbar=dict(title="Lg ERA",x=1.1)),
        hovertemplate = 'Lg K/BB: %{y:.2f}<extra></extra><br>' + '%{text}',
        text = ['LgERA: {}'.format(i) for i in league_pivot.ERA]))
    # team
    fig5.add_trace(go.Scatter(
        name='Team',
        x=team_pitching.yearID,
        y=team_pitching.KBB,
        mode='markers',
        marker=dict(symbol="circle", size=team_pitching.ERA, sizemode='area', 
            sizeref=2.*max(team_pitching.ERA)/(40.**2), color=team_pitching.ERA,
            showscale=True, reversescale=True, colorscale = 'Sunsetdark',
            colorbar=dict(title="Team ERA")),
        hovertemplate = 'Team K/BB: %{y:.2f}<extra></extra><br>' + '%{text}',
        text = ['Team ERA: {}'.format(i) for i in team_pitching.ERA]))
    # update figure options
    fig5.update_xaxes(title='Year', tickformat='d')
    fig5.update_yaxes(title='K/BB Ratio', nticks=len(team_pitching.ERA))
    fig5.update_layout(hovermode="x unified",title="Team K/BB Ratio with ERA Bubble",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    fig5.update_layout(legend=dict(orientation="h",
        yanchor="bottom",y=1.02,xanchor="right",x=1))
    # return figure
    return fig5


# top batters roster datatable
@app.callback(
    [Output('era-roster', 'data'),Output('era-roster','columns')],
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value')])
def update_roster_table(selected_team, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # select team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                        FROM teams team
                                        WHERE name = "{selected_team}"
                                            AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    # roster data
    roster = pd.read_sql_query(f'''SELECT DISTINCT batter.yearID, player.nameFirst || ' ' || player.nameLast AS playerName, fielder.POS, batter.G,
                                    batter.AB + batter.BB + IFNULL(batter.HBP,0) + IFNULL(batter.SH,0) + IFNULL(batter.SF,0) as PA,
                                    round((CAST(batter.H as FLOAT) + batter.BB + IFNULL(batter.HBP,0)) / (batter.AB + batter.BB + IFNULL(batter.HBP,0) + IFNULL(batter.SF,0)),3) as OBP,
                                    round(((CAST(batter.H as FLOAT) - batter."2B" - batter."3B" - batter.HR) + (batter."2B" * 2) + (batter."3B" * 3) + (batter.HR * 4)) / batter.AB,3) as SLG,
                                    fielder.InnOuts
                                    FROM batting batter
                                        LEFT JOIN fielding fielder ON fielder.playerID = batter.playerID
                                        LEFT JOIN people player ON player.playerID = batter.playerID
                                    WHERE batter.teamID = "{select_team_id['teamID'][0]}"
                                        AND batter.yearID >= {year_range[0]} AND batter.yearID <= {year_range[1]}
                                        AND fielder.POS != 'P'
                                    ORDER BY batter.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # drop 2020 as outlier
    roster = roster[roster.yearID != 2020].copy()
    # fill and replace
    roster_retype = roster.astype({'OBP': 'float', 'SLG': 'float'})
    roster_retype.fillna(0.0, inplace=True)
    roster_retype.replace({None: 0.0, '': 0.0}, inplace=True)
    # Set roster by position, sort by time at position ad batting performance
    first_list = roster_retype[roster_retype.POS == '1B'].sort_values(['InnOuts'],ascending=False).drop_duplicates(subset = ["playerName"])[0:10]
    first_list = first_list.sort_values(['PA'],ascending=False)[0:5]
    first_list = first_list.sort_values(['OBP'],ascending=False)[0:2]
    second_list = roster_retype[roster_retype.POS == '2B'].sort_values(['InnOuts'],ascending=False).drop_duplicates(subset = ["playerName"])[0:10]
    second_list = second_list.sort_values(['PA'],ascending=False)[0:5]
    second_list = second_list.sort_values(['OBP'],ascending=False)[0:2]
    short_list = roster_retype[roster_retype.POS == 'SS'].sort_values(['InnOuts'],ascending=False).drop_duplicates(subset = ["playerName"])[0:10]
    short_list = short_list.sort_values(['PA'],ascending=False)[0:5]
    short_list = short_list.sort_values(['OBP'],ascending=False)[0:2]
    third_list = roster_retype[roster_retype.POS == '3B'].sort_values(['InnOuts'],ascending=False).drop_duplicates(subset = ["playerName"])[0:10]
    third_list = third_list.sort_values(['PA'],ascending=False)[0:5]
    third_list = third_list.sort_values(['OBP'],ascending=False)[0:2]
    catch_list =  roster_retype[roster_retype.POS == 'C'].sort_values(['InnOuts'],ascending=False).drop_duplicates(subset = ["playerName"])[0:10]
    catch_list = catch_list.sort_values(['PA'],ascending=False)[0:5]
    catch_list = catch_list.sort_values(['OBP'],ascending=False)[0:2]
    of_list = roster_retype[roster_retype.POS == 'OF'].sort_values(['InnOuts'],ascending=False).drop_duplicates(subset = ["playerName"])[0:16]
    of_list = of_list.sort_values(['PA'],ascending=False)[0:10]
    of_list = of_list.sort_values(['SLG'],ascending=False)[0:6]
    # set dataframe of players
    position_player = pd.DataFrame()
    # append depreciated in v1.4 use concat instead
    # position_player = position_player.append([first_list, second_list, short_list, third_list, catch_list, of_list], ignore_index=True)
    position_player = pd.concat([first_list, second_list, short_list, third_list, catch_list, of_list], ignore_index=True)
    position_player.drop(['InnOuts'], axis=1,  inplace=True)
    position_player.drop_duplicates(keep='first', subset = ["playerName"], inplace=True)
    # Return player roster and data
    return position_player.to_dict('records'), [{'name': x, 'id': x} for x in position_player]


# starters pitching roster datatable
@app.callback(
    [Output('era-starters', 'data'),Output('era-starters','columns')],
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value')])
def update_starter_table(selected_team, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connection and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # select team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                        FROM teams team
                                        WHERE name = "{selected_team}"
                                            AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    # roster of pitchers
    roster = pd.read_sql_query(f'''SELECT DISTINCT pitcher.yearID, 
                                        player.nameFirst || ' ' || player.nameLast AS playerName,
                                        fielder.pos, pitcher.G, pitcher.SV,
                                        printf("%.3f", (CAST(pitcher.IPouts as FLOAT)) / (3)) as IP,
                                        printf("%.3f", (CAST(pitcher.W as FLOAT)) / (pitcher.W + pitcher.L)) as wPCT,
                                        printf("%.2f", CAST(pitcher.SO as FLOAT) / (pitcher.BB)) AS KBB,
                                        ERA
                                    FROM pitching pitcher
                                        LEFT JOIN fielding fielder ON fielder.playerID = pitcher.playerID AND fielder.pos = "P"
                                        LEFT JOIN people player ON player.playerID = pitcher.playerID
                                    WHERE pitcher.teamID = "{select_team_id['teamID'][0]}"
                                        AND pitcher.yearID >= {year_range[0]} AND pitcher.yearID <= {year_range[1]}
                                    ORDER BY pitcher.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # drop 2020 as outlier
    roster = roster[roster.yearID != 2020].copy()
    # reset data type 
    roster_retype = roster.astype({'IP': 'float', 'wPCT': 'float', 'KBB': 'float'})
    # fill and replace
    roster_retype.fillna(0.0, inplace=True)
    roster_retype.replace({None: 0.0}, inplace=True)
    # Sort roster by Innings pitched and ERA
    starter_list = roster_retype.sort_values(['IP'],ascending=False).drop_duplicates(subset = ["playerName"])[0:15]
    starter_list = starter_list.sort_values(['ERA'],ascending=True)[0:5]
    # set pitchers dataframe
    pitchers = pd.DataFrame()
    # concat roster to dataframe
    # pitchers = pitchers.append(starter_list, ignore_index=True)
    pitchers = pd.concat([starter_list], ignore_index=True)
    # Return pitchers and data
    return pitchers.to_dict('records'), [{'name': x, 'id': x} for x in pitchers]


# releif pitchers roster datatable
@app.callback(
    [Output('era-relief', 'data'),Output('era-relief','columns')],
    [Input('team-dropdown', 'value'),Input('era-dropdown', 'value')])
def update_bullpin_table(selected_team, selected_era):
    # select range
    year_range = dynamicrange(selected_era)
    # sql connect and query
    sqlite_con = sl.connect('data/lahmansbaseballdb.sqlite')
    # select team ID
    select_team_id = pd.read_sql_query(f'''SELECT DISTINCT team.teamID
                                        FROM teams team
                                        WHERE name = "{selected_team}"
                                            AND yearID >= {year_range[0]} AND yearID <= {year_range[1]};''',sqlite_con)
    # roster data
    roster = pd.read_sql_query(f'''SELECT DISTINCT pitcher.yearID, player.nameFirst || ' ' || player.nameLast AS playerName,
                                        fielder.pos, pitcher.G, pitcher.SV,
                                        printf("%.3f", (CAST(pitcher.IPouts as FLOAT)) / (3)) as IP,
                                        printf("%.3f", (CAST(pitcher.W as FLOAT)) / (pitcher.W + pitcher.L)) as wPCT,
                                        printf("%.2f", CAST(pitcher.SO as FLOAT) / (pitcher.BB + IFNULL(pitcher.IBB,0))) AS KBB,
                                        ERA
                                    FROM pitching pitcher
                                        LEFT JOIN fielding fielder ON fielder.playerID = pitcher.playerID AND fielder.pos = "P"
                                        LEFT JOIN people player ON player.playerID = pitcher.playerID
                                    WHERE pitcher.teamID = "{select_team_id['teamID'][0]}"
                                        AND pitcher.yearID >= {year_range[0]} AND pitcher.yearID <= {year_range[1]}
                                    ORDER BY pitcher.yearID ASC;''',sqlite_con)
    sqlite_con.close()
    # drop 2020 as outlier
    roster = roster[roster.yearID != 2020].copy()
    # retype roster data
    roster_retype = roster.astype({'IP': 'float', 'wPCT': 'float', 'KBB': 'float'})
    # fill and replace
    roster_retype.fillna(0.0, inplace=True)
    roster_retype.replace({None: 0.0}, inplace=True)
    # sort roster by saves and strikeout-walk ratio (K/BB)
    relief_list = roster_retype.sort_values(['SV'],ascending=False).drop_duplicates(subset = ["playerName"])[0:21]
    relief_list = relief_list.sort_values(['KBB'],ascending=False)[0:7]
    # set dataframe
    pitchers = pd.DataFrame()
    # concat relief pitchers data to dataframe
    # pitchers = pitchers.append(relief_list, ignore_index=True)
    pitchers = pd.concat([relief_list], ignore_index=True)
    # Return pitchers data
    return pitchers.to_dict('records'), [{'name': x, 'id': x} for x in pitchers]