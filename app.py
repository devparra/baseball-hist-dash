# Dash components, html, and io
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Plotly graph objects to render graph plots
import plotly.graph_objects as go
# Import Pandas
import pandas as pd

# Import custom data.py
import data

# Instantiate app with dash
app = dash.Dash(__name__)

# Title of applicaiton
app.title = 'MLB Historical Data Visualization'

# Import data from data.py file
teams_df = data.teams
# Hardcoded list that contain era names
era_list = data.era_list


# Applicaiton layout
app.layout = html.Div([
    # Banner DIV for dashboard
    html.Div([
        html.H1(children='Major League Baseball Team History'),
        html.H2(children='A Visualization of Historical Data')
    ],className='banner slice'),

    # Menu DIV, contains a dropdown list of Teams, set initial value to 'Boston Americans'
    html.Div([
        html.H2(children='Select an Era:'),
        dcc.Dropdown(
        className = 'era',
        id='era-dropdown',
        options=era_list,
        value=era_list[0]['value'],
        clearable=False),
        html.H3(children='All MLB Era\'s between 1903-2015 are represented.'),
        html.H2(children='Select A Team:'),
        dcc.Dropdown(
        className = 'team',
        id='team-dropdown',
        clearable=False),
        html.H3(children='All charts will show data from the selected team of given era.'),
    ],className='slice menu'),

    # Graphs of Historical Team statistics
    # Bar Chart of Wins and Losses
    dcc.Graph(className = 'slice feature', id='wl-bar', config={'displayModeBar': False}),
    # Line Chart of Batting Average, BABIP, and Strikeout Rate
    dcc.Graph(className = 'slice feature', id='batting-line', config={'displayModeBar': False}),
    # Pie Chart of % of Completed Games, Shutouts, and Saves of Total Games played
    dcc.Graph(className = 'slice feature2', id='pitch-pie', config={'displayModeBar': False}),
    # Line Bubble graph of K/BB ratio with ERA bubbles
    dcc.Graph(className = 'slice feature2', id='pitch-bubble', config={'displayModeBar': False}),
    # Line Char of Errors and Double Plays
    dcc.Graph(className = 'slice feature', id='feild-line', config={'displayModeBar': False}),

    # Footer with acknowledments
    html.Div([dcc.Markdown('''
    The data used in this app was retrieved from Kaggle and was created by code at
    [Benhamner's GitHub](https://github.com/benhamner/baseball). It is a processed version
    of the 2015 data at [Seanlahman.com](http://www.seanlahman.com/baseball-archive/statistics/).
    The original database was copyright 1996-2015 by Sean Lahman and licensed under a
    Creative Commons Attribution-ShareAlike 3.0 Unported License.
    For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
    '''),],className='slice copy'),
],className='page',)


# This is part of a standard callback that will hange the options of the team dropdown
@app.callback(
    Output('team-dropdown', 'options'),
    [Input('era-dropdown', 'value')])
def select_era(selected_era):
    # Change into lambda?
    if (selected_era == era_list[1]['value']):
        teams = data.dynamicteams(1)
    elif (selected_era == era_list[2]['value']):
        teams = data.dynamicteams(2)
    elif (selected_era == era_list[3]['value']):
        teams = data.dynamicteams(3)
    elif (selected_era == era_list[4]['value']):
        teams = data.dynamicteams(4)
    elif (selected_era == era_list[5]['value']):
        teams = data.dynamicteams(5)
    elif (selected_era == era_list[6]['value']):
        teams = data.dynamicteams(6)
    else:
        teams = data.dynamicteams(0)
    return teams


# The other half of the dropdown callback, this will provide the team dropdown with needed options
@app.callback(
    Output('team-dropdown', 'value'),
    [Input('team-dropdown', 'options')])
def set_team_value(available_options):
    return available_options[0]['value']


# Callback to a W-L Bar Chart, takes data request from dropdown
@app.callback(
    Output('wl-bar', 'figure'),
    [Input('team-dropdown', 'value')])
def update_figure1(selected_team):
    # Create filter dataframe of requested team data
    filter = teams_df[teams_df.name == selected_team]
    # Create Bar Chart figure, Wins and Losses
    fig1 = go.Figure(data=[
        go.Bar(name='Wins', x=filter.year, y=filter.w, marker_color='#004687'),
        go.Bar(name='Losses', x=filter.year, y=filter.l,  marker_color='#AE8F6F')
    ])
    # Update figure, set hover to the X-Axis and establish title
    fig1.update_layout(hovermode="x",barmode='group',title="Win/Loss Performance")
    # return figure
    return fig1


# Call back to Line Graph, takes data request from dropdown
@app.callback(
    Output('batting-line', 'figure'),
    [Input('team-dropdown', 'value')])
def update_figure2(selected_team):
    # Create filter dataframe of requested team data
    filter = teams_df[teams_df.name == selected_team]
    # Set a list of years team appear
    YR = filter.year
    # Set lists of team data
    AB = filter.ab
    Ht = filter.h
    SO = filter.so
    BB = filter.bb
    DBL = filter.double
    TRP = filter.triple
    HR = filter.hr
    # Calculate Strikeout Rate
    SOR = SO / AB
    # Calculate BABIP
    BABIP = (Ht - HR) / (AB - SO - HR)
    # Calculete Batting Average
    BAVG = Ht / AB
    # Create Line char figure using Strikeout Rate, BABIP, and Batting Average
    fig2 = go.Figure(data=[
        go.Scatter(name='Batting Average', x=filter.year, y=BAVG, mode='lines+markers', marker_color='#0C2C56'),
        go.Scatter(name='Balls (Hits) In Play', x=filter.year, y=BABIP, mode='markers', marker_color='#005C5C'),
        go.Scatter(name='Strikeout Rate', x=filter.year, y=SOR, mode='markers', marker_color='#D50032'),
    ])
    # Update layout, set hover to X-Axis and establish title
    fig2.update_layout(hovermode="x",title="Batting Performance")
    # Return figure
    return fig2


# Call back to Line Chart, Takes request data from dropdown menu
@app.callback(
    Output('feild-line', 'figure'),
    [Input('team-dropdown', 'value')])
def update_figure3(selected_team):
    # Create filter dataframe of requested team data
    filter = teams_df[teams_df.name == selected_team]
    # Create line chart figure using Errors and Double Plays
    fig3 = go.Figure(data=[
            go.Scatter(name='Errors', x=filter.year, y=filter.e, mode='markers', marker=dict(color='#5F259F')),
            go.Scatter(name='Double Plays', x=filter.year, y=filter.dp, mode='lines+markers', marker=dict(color='#005F61')),
    ])
    # Update Layout, set hover to X-Axis and establish title
    fig3.update_layout(hovermode="x",title="Feilding Performance")
    # return figure
    return fig3


# Call back to Pie Chart, takes data request from dropdown menu
@app.callback(
    Output('pitch-pie', 'figure'),
    [Input('team-dropdown', 'value')])
def update_figure4(selected_team):
    # Create filter dataframe of requested team data
    filter = teams_df[teams_df.name == selected_team]
    # Create a list of years the team appear
    YR = filter.year
    # Create lists of team data
    G = filter.g.sum()
    CG = filter.cg.sum() / G
    SHO = filter.sho.sum() / G
    SV = filter.sv.sum() / G
    # Set each list into a list (embedded list)
    PCT = [CG, SHO, SV]
    # Create Pie chart figure of Complete games, Shutouts, and saves
    fig4 = go.Figure(go.Pie(values=PCT,labels=['Complete Games','Shutouts','Saves'],))
    # Update Layout, set hover to false and establish title
    fig4.update_layout(hovermode=False,title="% of Total Games Played")
    # Update figure trace marker colors
    fig4.update_traces(marker=dict(colors=['#462425','#E35625','#CEC6C0']))
    # return figure
    return fig4


# Call back to Line Bubble Chart, take data request from dropdown menu
@app.callback(
    Output('pitch-bubble', 'figure'),
    [Input('team-dropdown', 'value')])
def update_figure3(selected_team):
    # Create filter dataframe of requested team
    filter = teams_df[teams_df.name == selected_team]
    # Create a list of years the team appear
    YR = filter.year
    # Create lists of team data
    ERA = filter.era
    SOA = filter.soa
    BBA = filter.bba
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
    fig5.update_layout(hovermode="x",title="K/BB v. ERA")
    # return figure
    return fig5


# runs main application in debug mode
if __name__ == '__main__':
    app.run_server(debug=True)
