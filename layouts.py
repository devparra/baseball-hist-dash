# Dash components, html, and dash tables
from dash import dcc
from dash import html
from dash import dash_table

# Import Bootstrap components
import dash_bootstrap_components as dbc

# Import custom data.py
from data.data import era_list


# Team Analysis
teamLayout = html.Div([
    # Title and page introduction
    dbc.Row(dbc.Col(html.H2(style={'text-align': 'center'}, children='Team Analysis by Era'))),
    html.Hr(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''To understand the future, we often look to the past. Major League Baseball 
        history goes back over 150 years, spanning and often reflecting American history. 
        Here the past is broken into popular Eras that represent the state of Major League 
        Baseball. Selecting from the leagues of the past as well as a team, you can view a 
        breakdown of Wins and Losses, Batting, and Pitching performances. Additionally we can 
        see a roster of players who were the most influential in the selected teams performance 
        during the preferred era.'''))),
    html.Br(),
    html.Hr(),
    # Era list dropdown
    dbc.Row([
            dbc.Col(html.H5(style = {'text-align': 'right', 'padding-right': '1em'},children='Select Era:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '13em'},
                id='era-dropdown',
                options=era_list,
                value=era_list[0]['value'],
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    # League list Dropdown
    dbc.Row([
            dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select League:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
                id='league-dropdown',
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})

    ]),
    # Team list dropdown
    dbc.Row([
            dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Team:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
                id='team-dropdown',
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})

    ]),
    html.Hr(),

    html.Br(),
    dbc.Row(dbc.Col(html.H4(children='Regular Season Analysis'))),
    # Wins and Losses
    dbc.Row(dbc.Col(dcc.Graph(id='wl-bar', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='The chart above breaks down the Wins and Losses, providing us perspective on the teams overall performance during regular season play.'))),
    # Line Chart of Batting Average, BABIP, and Strikeout Rate
    dbc.Row(dbc.Col(dcc.Graph(id='batting-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, compare the team's batting performance to league averages over the 
        chosen era. The BABIP (Batting Average on Balls In Play) analyzes a team's batting 
        average just on balls hit into the field of play, excluding outcomes that are not 
        influenced by the opposing defense. The OBP (On-Base Percentage) measures how often 
        the team reached base each plate appearance. Finally, the SLG (Slugging Average) 
        measures power representing the overall number of bases reached each at-bat by the 
        team.'''))),

    # Fielding
    dbc.Row(dbc.Col(dcc.Graph(id='feild-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, measure the teams fielding performance, the team's FPCT (Fielding Percentage) 
        is compared to the league average over the given era. The FPCT gauges how frequently a 
        team can "make the play."'''))),
    
    # K/BB ratio with ERA bubbles
    dbc.Row([dbc.Col(dcc.Graph(id='pitch-bubble', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0}),],),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, analye the pitching performance of the team. We look at the 
        K/BB (Strikeout-to-Walk Ratio) that is defined by a bubble which grows with the teams 
        ERA (Earned Run Average) and compares to the league average over the selected era. 
        The number of earned runs allowed by the team per nine innings is represented by the 
        ERA. While the K/BB ratio indicates how many strikeouts the team records for each 
        walk allowed.'''))),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(html.H4(children='Postseason Record'))),
    html.Hr(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Below we have a quick look at the team's postseason journey during the 
        selected era. It should be noted that divisional play did not start until the 1995 
        MLB realignment. The Wildcard was introduced in 1995, however the Wild Card Series 
        was not played until 2012. The MLB League Championship series did not start until 
        1969 when the American League expanded to twelve teams. The first World Series was 
        not held until 1903, the "best-of-seven" World Series was introduced in 1905.'''))),
    html.Br(),
    # team chamionship data
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='team-champ',
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
                }
        ), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
                xl={'size':10, 'offset':0}),justify="center"),

    html.Br(),
    # team postseason data
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='team-post-table',
            style_as_list_view=True,
            editable=False,
            style_table={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflowY': 'scroll',
                'width': 'auto',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '4px',
                }
        ), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':12, 'offset':0}, lg={'size':12, 'offset':0},
                xl={'size':12, 'offset':0}),justify="center"),
    html.Br(),
    html.Br(),
    # Era roster of top players
    dbc.Row(dbc.Col(html.H4(children='Era Top Performers Roster'))),
    html.Hr(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''This is a roster of top players who were the most noteworthy in the 
        selected teams performance during the preferred era. All players are evaluated for 
        their statistical performance then listed based on the most significant year of 
        performance within the selected Era. To evaluate and discern between position players 
        we looked at the number of innings played at each position. Next we look at each 
        players PA (Plate Appearances) then evaluate their OBP (On-Base Percentage) and 
        SLG (Slugging Average). Some calculations were adjusted to reflect that some 
        statistics were not tracked until 1955. Starting pitchers are evaluated based on 
        the number of Innings pitched and their ERA (Earned Run Average) while relief 
        pitchers are evaluated on the number of games saved as well as their 
        K/BB (Strikeout-to-Walk Ratio). Some positions may be missing due to players 
        who played multiple positions.'''))),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(html.H4(children="Position Players"))),
    html.Br(),
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='era-roster',
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
                }),
            xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
            xl={'size':10, 'offset':0}),justify="center"),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(html.H4(children="Starting Pitchers"))),
    html.Br(),
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='era-starters',
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
                }),
            xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
            xl={'size':10, 'offset':0}),justify="center"),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(html.H4(children="Relief Pitchers"))),
    html.Br(),
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='era-relief',
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
                }),
            xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
            xl={'size':10, 'offset':0}),justify="center")

])


# Roster Analysis
rosterLayout = html.Div([
    # Title and description
    dbc.Row(dbc.Col(html.H2(style={'text-align': 'center'}, children='Roster Analysis'))),
    html.Hr(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''To understand the success of any team, we need to look at how that team 
        is constructed. This page gives us a look at the selected teams roster and how the 
        players influenced the team and the selected session during the chosen era.'''))),
    html.Br(),
    html.Hr(),
    # Era Dropdown
    dbc.Row([
        dbc.Col(html.H5(style = {'text-align': 'right', 'padding-right': '1em'},children='Select Era:'),
            xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style = {'text-align': 'center', 'font-size': '1em', 'width': '13em'},
            id='era-dropdown',
            options=era_list,
            value=era_list[0]['value'],
            clearable=False),
            xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    # League Dropdown
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select League:'),
            xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
            id='league-select-dropdown',
            clearable=False),
            xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    # Team Dropdown
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Team:'),
            xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
            id='team-select-dropdown',
            clearable=False),
            xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    # Roster Year dropdown
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Roster Year:'), xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style={'text-align': 'center', 'font-size': '1em', 'width': '6em'},
            id='year-select-dropdown',
            clearable=False
            ), xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    html.Hr(),

    # GRAPH FOR DISTROBUTION OF RUNS CREATED
    dbc.Row(dbc.Col(dcc.Graph(id='roster-rc-dist', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, we have a distribution of position players runs created. The 
        Runs Created statistic shows how many runs have been generated by a player's 
        actions at the plate and on the basepath. For modern players we can consider the 
        “Technical” formula found on FanGraphs. Since certain statistics were not maintained 
        until 1955, we use the “Basic” formula.'''))),

    # GRAPH FOR ERA FOR PITCHERS
    dbc.Row(dbc.Col(dcc.Graph(id='roster-era-dist', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above we can see a representation of the pitching staff, comparing each 
        player's K/BB (Strikeout to Walk Ratio) defining each point with a bubble determined 
        by their player’s respective ERA (Earned Run Average).'''))),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Below we can select a position to explore along with a player. 
        Certain statistics are represented below plotting each player's career over 
        the selected era, highlighting the selected roster year.'''))),
    
    # SELECT POSITION
    html.Br(),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Player:'), xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style={'text-align': 'center', 'font-size': '1em', 'width': '13em', 'justify-self': 'right'},
            id='pos-dropdown',
            clearable=False
            ), xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    # Select Player
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Player:'), xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style={'text-align': 'center', 'font-size': '1em', 'width': '13em', 'justify-self': 'right'},
            id='player-dropdown',
            clearable=False
            ), xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    html.Hr(),

    #Player datatable
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(id='player-data-tabel')
    ,xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':10, 'offset':0}, 
    lg={'size':12, 'offset':0}, xl={'size':12, 'offset':0})
    ],justify="center"),

    # Batting Graph
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Graph(id='player-batting-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    # Player batting
    dbc.Row([
        dbc.Col(
            html.Div(id='player-batting-tabel')
    ,xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':10, 'offset':0}, 
    lg={'size':12, 'offset':0}, xl={'size':12, 'offset':0})
    ],justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above we compare the selected players batting statistics to league 
        averages over the selected era. The player’s BABIP (Batting Average on Balls in Play) 
        gives us an idea on how consistent the player is at the plate while the 
        OBP (On-Base Percentage) tells us how often they reach base each plate appearance. 
        The player's SLG (Slugging Average) tells us how much they hit for power. 
        Additionally we have a look at the players statistics for the selected year 
        providing us with deeper detail into their contribution.'''))),
    
    # Fielding Graph
    dbc.Row(dbc.Col(dcc.Graph(id='player-fielding-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    # Player Fielding
    dbc.Row([
        dbc.Col(
            html.Div(id='player-field-tabel')
    ,xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':10, 'offset':0}, 
    lg={'size':12, 'offset':0}, xl={'size':12, 'offset':0})
    ],justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, the FPCT (Fielding Percentage) of the selected player is compared 
        to the league average over the selected era. We also have a survey of the selected 
        players fielding statistics highlighting their ability at their respective position.'''))),

    # Pitching graph
    dbc.Row(dbc.Col(html.Div(id='player-pitching-graph'), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0},
        md={'size':12, 'offset':0}, lg={'size':12, 'offset':0}, xl={'size':12, 'offset':0})),
    # player pitching
    dbc.Row([
        dbc.Col(
            html.Div(id='player-pitch-tabel')
    ,xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':10, 'offset':0}, 
    lg={'size':12, 'offset':0}, xl={'size':12, 'offset':0})
    ],justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, the selected players K/BB (Strikeout to Walk Ratio) with 
        ERA (Earned Run Average) bubble is mapped over the selected era, comparing the 
        player to the league average. Furthermore, the player’s pitching statistics for 
        the selected year is provided for further analysis.'''))),
])


# Team V Team
teamVLayout = html.Div([
    # Title and description
    dbc.Row(dbc.Col(html.H2(style={'text-align': 'center'}, children='Team Vs Team Analysis'))),
    html.Hr(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''The rivalry is rooted in the long history of baseball, from New York 
        versus Boston to Los Angeles versus San Francisco, these feuds fill each team's stands 
        with anxious fans. Comparing teams for postseason consideration has prompted debate 
        since the turn of the last century. This page provides a window into baseball history 
        and its many rivalries. By selecting an Era, we can choose and compare teams from 
        around the leagues.'''))),
    html.Br(),
    # Era Dropdown
    html.Hr(),
    dbc.Row([
            dbc.Col(html.H5(style = {'text-align': 'right', 'padding-right': '1em'},children='Select Era:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '13em'},
                id='era-dropdown',
                options=era_list,
                value=era_list[0]['value'],
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    # League A dropdown
    dbc.Row([
            dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select League One:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
                id='league-one-dropdown',
                value='AL',
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    # Team A Dropdown
    ]),
    dbc.Row([
            dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Team One:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
                id='team-one-dropdown',
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    # League B Dropdown
    ]),
    dbc.Row([
            dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select League Two:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
                id='league-two-dropdown',
                value='NL',
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    # Team B Dropdown
    ]),
    dbc.Row([
            dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Team Two:'),
                xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
                lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
            dbc.Col(dcc.Dropdown(
                style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
                id='team-two-dropdown',
                clearable=False),
                xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
                lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})

    ]),
    html.Hr(),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Below is a brief look at each teams postseason title count along with a 
        look at each respective parks Average Park Factor and a Combined Average Attendance.'''))),
    
    html.Br(),
    # team A data datatables
    dbc.Row([dbc.Col(
        dash_table.DataTable(
            id='team-one-champ',
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
                    'padding': '4px',
                }
        ), xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':6, 'offset':0}, lg={'size':6, 'offset':0},
                xl={'size':6, 'offset':0}),
            dbc.Col(
        dash_table.DataTable(
            id='team-two-champ',
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
                    'padding': '4px',
                }
        ), xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':6, 'offset':0}, lg={'size':6, 'offset':0},
                xl={'size':6, 'offset':0})],justify="center"),
    html.Br(),

    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''The Park Factor displays the observed effect of each shown stat on the 
        selected park's events. Each value is set to "100" to represent the average for that 
        metric. A park above 100 would be favorable for batters while below 100 would be 
        favorable for pitchers. For our purpose we averaged all park factors for the selected 
        era. To gain a perspective on the team's popularity with fans we can look at the 
        Combined Average Attendance.'''))),
    html.Br(),
    # team B data datatables
    dbc.Row([dbc.Col(
        dash_table.DataTable(
            id='team-one-table',
            style_as_list_view=True,
            editable=False,
            style_table={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflowY': 'scroll',
                'width': 'auto',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '4px',
                }
        ), xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':6, 'offset':0}, lg={'size':6, 'offset':0},
                xl={'size':6, 'offset':0}),
        dbc.Col(
        dash_table.DataTable(
            id='team-two-table',
            style_as_list_view=True,
            editable=False,
            style_table={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflowY': 'scroll',
                'width': 'auto',
            },
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '4px',
                }
        ), xs={'size':6, 'offset':0}, sm={'size':6, 'offset':0}, md={'size':6, 'offset':0}, lg={'size':6, 'offset':0},
                xl={'size':6, 'offset':0})],justify="center"),
    
    # WL graph
    dbc.Row(dbc.Col(dcc.Graph(id='teamv-wl-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''The graph above compares each team’s Winning Percentage (wPCT) over 
        the selected era. Combining the wins and losses of the team we gain a 
        percentage that provides us perspective on a teams performance in the regular 
        season.'''))),
    # Batting Graph
    dbc.Row(dbc.Col(dcc.Graph(id='teamv-batting-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, compare each team’s batting performance by looking at some factors. 
        First contrasting each team's BABIP (Batting Average on Balls in Play), we can gain a 
        sense of how consistent each team was at the plate. Next, the OBP (On-Base Percentage) 
        can provide us information on the frequency with which each team reached base each 
        plate appearance. Finally,  with the SLG (Slugging Average) we can compare each team's 
        ability to hit for power.'''))),
    # Feilding Graph
    dbc.Row(dbc.Col(dcc.Graph(id='teamv-field-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''The above graph provides us with a look at each team's FPCT (Fielding Percentage) enabling us to compare each team's ability to “make the play”.'''))),
    # Pitching Graph
    dbc.Row(dbc.Col(dcc.Graph(id='teamv-pitch-line', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px','margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Finally, the graph above shows us each team’s ERA (Earned Run Average) over the selected era, providing a perspective on each team’s pitching ability.'''))),
])


# Regression Layout
regLayout = html.Div([
    # Title and description
    dbc.Row(dbc.Col(html.H2(style={'text-align': 'center'}, children='Regression Analysis'))),
    html.Hr(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''For any team it is important not only to know where you have been but also 
        where you are going. Evaluating individual players' statistics can provide an idea as 
        to their impact on a team or their impact on opponents in the future. Regression 
        analysis is a set of statistical methods for estimating relationships between an 
        independent variable and a dependent variable. For our purposes we will look at 
        regressions with time series but also a correlation regression. The most common 
        methodologies for investigating the relationship between two quantitative variables 
        are correlation and linear regression. Since the data can be plotted over time we can 
        use time series analysis, which helps identify the underlying causes of trends or 
        systemic patterns over time.'''))),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Below a list of 100 players is generated based on whether or not they 
        played more than two thirds of the last season, their performance over the last 
        season, and if they have played at least 7 seasons. The list is generated from the most 
        recent data available in the database, some players may no longer be active. 
        Select from the list to evaluate.'''))),
    # Neccesary to initiate select_top_player callback
    html.P(id='none'),
    html.Hr(),
    # Top players dropdown
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Select Player:'), xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style={'text-align': 'center', 'font-size': '1em', 'width': '13em', 'justify-self': 'right'},
            id='top-player-dropdown',
            clearable=False
            ), xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    html.Hr(),
    # player datatable
    html.Br(),
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='top-player-info-tabel',
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
                }
        ), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
                xl={'size':10, 'offset':0}),justify="center"),
    html.Br(),
    # Batting datatable
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='top-player-data-tabel',
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
                }
        ), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
                xl={'size':10, 'offset':0}),justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Each player’s 2020 season will be dropped from the analysis as an outlier 
        season. Each player will have 5 seasons analyzed and a prediction rendered as well as 
        visualizations of each area of analysis. Below is a 162 game average of the selected 
        player. An effort to fit each batter's lifetime statistics into a single season, providing 
        an overall perspective of the players career averaged over 162 games.'''))),
    html.Br(),
    # 162 game career average table
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='top-player-caravg-tabel',
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
                }
        ), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
                xl={'size':10, 'offset':0}),justify="center"),
    html.Br(),
    # dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
    #     children=''''''))),
    html.Hr(),
    # Regression selection dropdown
    dbc.Row([
        dbc.Col(html.H5(style={'text-align': 'right', 'padding-right': '1em'}, children='Regression Method:'),
            xs={'size':5, 'offset':0}, sm={'size':5, 'offset':0}, md={'size':5, 'offset':0},
            lg={'size':5, 'offset':0}, xl={'size':5, 'offset':0}),
        dbc.Col(dcc.Dropdown(
            style = {'text-align': 'center', 'font-size': '1em', 'width': '12em', 'justify-self': 'left'},
            id='reg-dropdown',
            options=['Time Step','Lag Method', 'Corr Method'],
            value='Time Step',
            clearable=False),
            xs={'size':3, 'offset':0}, sm={'size':3, 'offset':0}, md={'size':3, 'offset':0},
            lg={'size':3, 'offset':0}, xl={'size':3, 'offset':0})
    ]),
    html.Hr(),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Select a regression method above to determine how a player will be evaluated.
        By default Time Step analysis is selected, for this we created a time-step feature that 
        can be calculated directly from the time index. The time dummy is the most fundamental 
        time-step feature, ticking off time steps in a series from start to finish. Next we can 
        select a Time Lag analysis, the lag is used to move the observations in the target series 
        so that they appear to have occurred later in time. For our purpose, we've added a 1-step 
        lag feature. Finally we can analyze players based on the correlation of the choice 
        statistics with which we have chosen to evaluate each player by selecting the Corr Method 
        (correlation analysis method). The linear regression can be applied to each analysis 
        method providing different yet valuable perspectives on the selected players future performance. '''))),
    # Player prediction datatable
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'font-weight': '500', 'margin': 'auto', 'width': '90%', 'opacity': '80%'}, children='Player Predictions'))),
    html.Br(),
    dbc.Row(dbc.Col(
        dash_table.DataTable(
            id='top-player-pred-tabel',
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
                }
        ), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size':10, 'offset':0}, lg={'size':10, 'offset':0},
                xl={'size':10, 'offset':0}),justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above are the result predictions of the selected regression method. 
        Below are visualizations providing information on the selected regression method.'''))),
    html.Br(),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Below, we have an analysis of Games, Plate Appearances, and Technical 
        Runs Created by the selected player. The time-step method will provide a 
        regression of each season over the past 5 years, plotting actual statistics and 
        estimated (predicted) statistics. The lag method will supply a regression allowing 
        us to model any serial dependence while also plotting actual and predicted 
        statistics. Finally the correlation method will yield a regression of statistics 
        that is correlated to one another. Hover the mouse over each prediction to view 
        more information about the regression.'''))),
    # Games regression
    dbc.Row(dbc.Col(dcc.Graph(id='g-regression', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, games are analyzed with either the time-step, lag, or correlation 
        method. If the correlation method is selected, the plot will display games played 
        plotted over a time-step with the 50th quantile (median) mapped as a horizontal line. For our 
        purpose we will assume the selected player will start the latest season in peak health 
        and provide their highest performance for duration. To calculate the best possible 
        outcome, each season above the 50th quantile is kept along with an additional 162 game 
        season to ensure the final average is weighted in favor of a “peak” season. A player's 
        predicted season will never reflect more than 162 games.'''))),
    # Plate Apperences regression
    dbc.Row(dbc.Col(dcc.Graph(id='pa-regression', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, Plate Apperences (PA) are analyzed with either the time-step, lag, or correlation 
        method. If the correlation method is selected, Plate Appearances will be plotted over 
        Games. The correlation method assumes the player will provide a peak season of 
        performance.'''))),

    # Tech. Runs Created regression
    dbc.Row(dbc.Col(dcc.Graph(id='trc-regression', config={'displayModeBar': False}), xs={'size':12, 'offset':0}, sm={'size':12, 'offset':0}, md={'size': 12, 'offset': 0},lg={'size': 12, 'offset': 0})),
    dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'},
        children='''Above, Technical Runs Created (tRC) are analyzed with either the time-step, lag, or 
        correlation method. If the correlation method is selected, Technical Runs Created 
        will be plotted over Plate Appearances. The correlation method assumes the player 
        will provide a peak season of performance.'''))),

    # Stores the intermediate values from the batting datatable
    dcc.Store(id='intermediate-data')
])