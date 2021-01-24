# import dash IO and graph objects
from dash.dependencies import Input, Output
import plotly.graph_objects as go
# import app
from app import app

# Import custom data.py
import data
# Import team data from data.py file
teams_df = data.teams
# Hardcoded list that contain era names
era_list = data.era_list
# Batters data
batter_df = data.batters


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
    filter = teams_df[teams_df.name == selected_team]
    # This feels like a hack
    # Checks if year_range is empty (NonType)
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        # I created this becuase i kept getting NonType errors with all of my graph call backs
        # Set year range to default position
        year_range = [1903,1919]
        # Filter the years of the data to be within range
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
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
    # Create filter dataframe of requested team data
    filter = teams_df[teams_df.name == selected_team]
    # This still feels like a hack
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
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
    filter = teams_df[teams_df.name == selected_team]
    # Im pretty sure this is a hack, there has to be a different approch
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
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
    filter = teams_df[teams_df.name == selected_team]
    # IDK what to say, this is needed untill i can fix it.
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
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
    filter = teams_df[teams_df.name == selected_team]
    # I will revisit this again soon, it just doesnt seem efficient
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        year_range = [1903,1919]
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
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
    filter = teams_df[teams_df.name == selected_team]
    # I will revisit this again soon, it just doesnt seem efficient
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        # year_range = [1903,1919]
        filter_year = filter[( filter.year >= 1903 )&( filter.year <= 1919 )]

    Data = filter_year.drop(columns=['team_id', 'g', 'w', 'l', 'r', 'ab', 'h', 'double', 'triple',
        'hr', 'bb', 'so', 'sb', 'cs', 'era', 'cg', 'sho', 'sv', 'ha', 'hra', 'bba', 'soa', 'e', 'dp',
        'fp', 'name', 'park'])

    return Data.to_dict('records'), [{'name': x, 'id': x} for x in Data]


# callback to data-table of player batting performance
# NOTE: this callback will need to be updated to reflect proper year span (Era)
@app.callback(
    [Output('batterTable', 'data'),Output('batterTable','columns')],
    [Input('team-dropdown', 'value'),Input('era-slider', 'value')])
def update_batter_table(selected_team, year_range):
    # Create filter dataframe of requested team
    filter = teams_df[teams_df.name == selected_team]
    # I will revisit this again soon, it just doesnt seem efficient
    if year_range:
        filter_year = filter[( filter.year >= year_range[0] )&( filter.year <= year_range[1] )]
    else:
        # year_range = [1903,1919]
        filter_year = filter[( filter.year >= 1903 )&( filter.year <= 1919 )]
    # obtain team id from filter
    id = filter_year.team_id
    # apply filtered team id to batters dataframe
    Batters = batter_df[batter_df.team_id == id.iloc[0]]

    # returns batters dataframe as dictionary and returns a key value pair for column headers
    return Batters.to_dict('records'), [{'name': x, 'id': x} for x in Batters]
