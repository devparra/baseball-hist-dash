# import dash IO and graph objects
from dash.dependencies import Input, Output
import plotly.graph_objects as go
# import app
from app import app
# import pandas
import pandas as pd

# Import custom data.py
import data

# Import data from data.py file
teams_df = data.teams
# Hardcoded list that contain era names
era_list = data.era_list
# Batters data
batter_df = data.batters
# Player Profiles data
player_df = data.players

team_players_df = data.team_players


# This will update the team dropdown and the range of the slider
@app.callback(
    [Output('team-dropdown', 'options'),
    Output('team-dropdown', 'value'),
    Output('era-slider', 'value'),],
    [Input('era-dropdown', 'value')])
def select_era(selected_era):
    # Change into lambda? May make it unreadable
    # Check if selected era is equal to the value in the era list
    # Makes sure that teams and range are set to desired era
    if (selected_era == era_list[1]['value']):
        teams = data.dynamicteams(1)
        range = data.dynamicrange(1)
    elif (selected_era == era_list[2]['value']):
        teams = data.dynamicteams(2)
        range = data.dynamicrange(2)
    elif (selected_era == era_list[3]['value']):
        teams = data.dynamicteams(3)
        range = data.dynamicrange(3)
    elif (selected_era == era_list[4]['value']):
        teams = data.dynamicteams(4)
        range = data.dynamicrange(4)
    elif (selected_era == era_list[5]['value']):
        teams = data.dynamicteams(5)
        range = data.dynamicrange(5)
    elif (selected_era == era_list[6]['value']):
        teams = data.dynamicteams(6)
        range = data.dynamicrange(6)
    else:
        teams = data.dynamicteams(0)
        range = data.dynamicrange(0)
    # Return team list, the initial value of the team list, and the range in the era
    return teams, teams[0]['value'], range


# Callback to a W-L Bar Chart, takes data request from dropdown
@app.callback(
    Output('wl-bar', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_figure1(selected_team, year_range):
    filter_team = teams_df[teams_df.team_id == selected_team]
    # This feels like a hack
    # Checks if year_range is empty (NonType)
    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        # I created this becuase i kept getting NonType errors with all of my graph callbacks
        # Set year range to default position
        year_range = [1903,1919]
        # Filter the years of the data to be within range
        filter_year = filter[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    # Create Bar Chart figure, Wins and Losses
    fig1 = go.Figure(data=[
        go.Bar(name='Wins', x=filter_year.year, y=filter_year.w, marker_color='#004687'),
        go.Bar(name='Losses', x=filter_year.year, y=filter_year.l,  marker_color='#AE8F6F')
    ])
    # Update figure, set hover to the X-Axis and establish title
    fig1.update_layout(hovermode="x",barmode='group',title="Win/Loss Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    # return figure
    return fig1


# Call back to batting performance line graph, takes data request from dropdown
@app.callback(
    Output('batting-line', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_figure2(selected_team, year_range):
    filter_team = teams_df[teams_df.team_id == selected_team]
    # This still feels like a hack
    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        # Default range position
        year_range = [1903,1919]
        # Filter the years of the data to be within range
        filter_year = filter[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    # Set a list of years team appear
    YR = filter_year.year
    # Set lists of team data
    AB = filter_year.ab
    Ht = filter_year.h
    SO = filter_year.so
    BB = filter_year.bb
    DBL = filter_year.double
    TRP = filter_year.triple
    HR = filter_year.hr
    # Calculate Strikeout Rate
    SOR = SO / AB
    # Calculate BABIP
    BABIP = (Ht - HR) / (AB - SO - HR)
    # Calculete Batting Average
    BAVG = Ht / AB
    # Create Line char figure using Strikeout Rate, BABIP, and Batting Average
    fig2 = go.Figure(data=[
        go.Scatter(name='Batting Average', x=filter_year.year, y=BAVG, mode='lines+markers', marker_color='#0C2C56'),
        go.Scatter(name='Balls (Hits) In Play', x=filter_year.year, y=BABIP, mode='markers', marker_color='#005C5C'),
        go.Scatter(name='Strikeout Rate', x=filter_year.year, y=SOR, mode='markers', marker_color='#D50032'),
    ])
    # Update layout, set hover to X-Axis and establish title
    fig2.update_layout(hovermode="x",title="Batting Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    # Return figure
    return fig2


# Call back to Line Chart of feilding performance, Takes request data from dropdown menu
@app.callback(
    Output('feild-line', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_figure3(selected_team, year_range):
    # Create filter dataframe of requested team data
    filter_team = teams_df[teams_df.team_id == selected_team]
    # Im pretty sure this is a hack, there doesn't seem to be a different approch
    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        # Filter the years of the data to be within range
        filter_year = filter[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    # Create line chart figure using Errors and Double Plays
    fig3 = go.Figure(data=[
            go.Scatter(name='Errors', x=filter_year.year, y=filter_year.e, mode='markers', marker=dict(color='#5F259F')),
            go.Scatter(name='Double Plays', x=filter_year.year, y=filter_year.dp, mode='lines+markers', marker=dict(color='#005F61')),
    ])
    # Update Layout, set hover to X-Axis and establish title
    fig3.update_layout(hovermode="x",title="Feilding Performance",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    # return figure
    return fig3


# Call back to Pie Chart of total games played, takes data request from dropdown menu
@app.callback(
    Output('pitch-pie', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_figure4(selected_team, year_range):
    # Create filter dataframe of requested team data
    filter_team = teams_df[teams_df.team_id == selected_team]
    # IDK what to say...
    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        # Filter the years of the data to be within range
        filter_year = filter[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    # Create a list of years the team appear
    YR = filter_year.year
    # Create lists of team data
    # Prevents a RuntimeError: invalid value encountered in longlong_scalars
    if (filter_year.g.sum() == 0):
        G = 1
    else:
        G = filter_year.g.sum()
    CG = filter_year.cg.sum() / G
    SHO = filter_year.sho.sum() / G
    SV = filter_year.sv.sum() / G
    # Set each list into a list (embedded list)
    PCT = [CG, SHO, SV]
    # Create Pie chart figure of Complete games, Shutouts, and saves
    fig4 = go.Figure(go.Pie(values=PCT,labels=['Complete Games','Shutouts','Saves'],))
    # Update Layout, set hover to false and establish title
    fig4.update_layout(hovermode=False,title="% of Total Games Played",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    # Update figure trace marker colors
    fig4.update_traces(marker=dict(colors=['#462425','#E35625','#CEC6C0']))
    # return figure
    return fig4


# callback to the bubble chart of strikeout/walk ratio and era, takes data requests from dropdown menu
@app.callback(
    Output('pitch-bubble', 'figure'),
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_figure5(selected_team, year_range):
    # Create filter dataframe of requested team
    filter_team = teams_df[teams_df.team_id == selected_team]
    # I will revisit this again soon, it just doesnt seem efficient
    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        filter_year = filter[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    # Create a list of years the team appear
    YR = filter_year.year
    # Create lists of team data
    ERA = filter_year.era
    SOA = filter_year.soa
    BBA = filter_year.bba
    # Calculate K/BB ratio
    RATIO = SOA / BBA
    # Create line chart of K/BB ratio with ERA used for bubble size
    fig5 = go.Figure(data=go.Scatter(
        x=YR,
        y=RATIO,
        mode='markers',
        marker=dict(symbol="circle-open-dot", size=5.*ERA, color='#006BA6',),
        hovertemplate = 'K/BB: %{y:.2f}<extra></extra><br>' + '%{text}',
        text = ['ERA: {}'.format(i) for i in ERA]))
    # Update layout, set hover to x-axis and establish title
    fig5.update_layout(hovermode="x",title="K/BB v. ERA",
        font={'color':'darkslategray'},paper_bgcolor='white',plot_bgcolor='#f8f5f0')
    # return figure
    return fig5


# callback to data-table of team accolades
@app.callback(
    [Output('table', 'data'),Output('table','columns')],
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_table(selected_team, year_range):
    # Create filter dataframe of requested team
    filter_team = teams_df[teams_df.team_id == selected_team]

    if year_range:
        filter_year = filter_team[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        filter_year = filter[( filter_team.year >= year_range[0] )&( filter_team.year <= year_range[1] )]

    # remove unneccesary columns
    # only want accolades
    Data = filter_year.drop(columns=['team_id', 'g', 'w', 'l', 'r', 'ab', 'h', 'double', 'triple',
        'hr', 'bb', 'so', 'sb', 'cs', 'era', 'cg', 'sho', 'sv', 'ha', 'hra', 'bba', 'soa', 'e', 'dp',
        'fp', 'name', 'park'])
    # Check if the team won a world series
    WIN = Data[Data.ws_win == 'Y']
    # if empty, no world series won
    if WIN.empty:
        # Check if the team won a wild card, will only apply to teams in the 2000s
        WIN = Data[Data.wc_win == 'Y']
        # if empty, no wild cards won
        if WIN.empty:
            # Check if the team won a division series, lowest level of championship in MLB
            WIN = Data[Data.div_win == 'Y']
            # if the team won a division but no league title the data will still show
            # if the team won the league by winning a wild card but not world series, the data
            # will still show
            # it stands to reason that if any championship is won, the data will reflect in the datatable

    # return win as dictionary to data and the key value pair to the columns
    return WIN.to_dict('records'), [{'name': x, 'id': x} for x in WIN]


# Dynamically create a list of ballplayers will known name (not given name) and player id based on team and era
@app.callback(
    [Output('player-dropdown', 'options'), Output('player-dropdown', 'value')],
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_player_dropdown(selected_team, year_range):
    # Select team
    team = team_players_df[team_players_df.team_id == selected_team]
    # Check/filter year range
    if year_range:
        filter_year = team[(team.year >= year_range[0])&(team.year <= year_range[1])]
    else:
        filter_year = team[(team.year >= 1903 )&(team.year <= 1919 )]
    # Use known names to set a key value pair for dropdown
    names = [{'label': k, 'value': v }for k, v in zip(filter_year.known_name, filter_year.player_id)]
    # Set new list
    player_list = []
    # append list with unique names, prevents duplicate entries
    # Using unique function in pandas removes names that are supposed to be included
    [player_list.append(x) for x in names if x not in player_list]
    # Return given name key value pair to options and value of dropdown
    return player_list, player_list[0]['value']


@app.callback(
    [Output('playerProfile', 'data'),Output('playerProfile','columns')],
    [Input('player-dropdown', 'value')])
def update_profile_table(player):
    # Create player filter with selected player
    filter_player = player_df[player_df.player_id == player]
    # drop unneccesary columns
    data_filter = filter_player.drop(columns=['player_id', 'name_first', 'name_last',
        'name_given', 'retro_id', 'bbref_id', 'birth_month', 'birth_day',
        'birth_country', 'birth_city', 'birth_state', 'death_month', 'death_day',
        'death_country', 'death_city', 'death_state',])
    # Return batters dictionary to data and batters key value pair to columns
    return data_filter.to_dict('records'), [{'name': x, 'id': x} for x in data_filter]


@app.callback(
    [Output('batterTable', 'data'),Output('batterTable','columns')],
    [Input('player-dropdown', 'value'),Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_batter_table(player, selected_team, year_range):
    # take in the selected team
    filter_team = batter_df[batter_df.team_id == selected_team]
    # Set year range
    if year_range:
        filter_year = filter_team[(filter_team.year >= year_range[0] )&(filter_team.year <= year_range[1] )]
    else:
        filter_year = filter_team[(filter_team.year >= 1903 )&(filter_team.year <= 1919 )]
    # Apply filter player and team id to batters dataframe
    filter_batter = filter_year[filter_year.player_id == player]
    # drop unneccesary columns
    data_filter = filter_batter.drop(columns=['player_id', 'team_id', 'stint', 'league_id'])
    # Return batters dictionary to data and batters key value pair to columns
    return data_filter.to_dict('records'), [{'name': x, 'id': x} for x in data_filter]
