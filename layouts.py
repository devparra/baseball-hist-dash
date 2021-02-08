# Dash components, html, and io
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Import custom data.py
import data

# Import data from data.py file
teams_df = data.teams
# Hardcoded list that contain era names
era_list = data.era_list
era_marks = data.era_marks


# App main menu
appMenu = html.Div([
        html.H2(children='Select an Era:'),
        dcc.Dropdown(
            className = 'era',
            id='era-dropdown',
            options=era_list,
            value=era_list[0]['value'],
            clearable=False),
        html.H4(children='All MLB Era\'s between 1903-2015 are represented.'),
        html.H2(children='Select A Team:'),
        dcc.Dropdown(
            className = 'team',
            id='team-dropdown',
            clearable=False),
        html.H4(children='Available teams are updated based on Era selection.'),
        dcc.RangeSlider(
            id='era-slider',
            className='era-slider',
            min=teams_df[teams_df.year == 1903].iloc[0].year,
            max=teams_df['year'].max(),
            marks=era_marks,
            tooltip={'always_visible': False, 'placement': 'bottom'},),
        html.H4(children='Adjust slider to desired range.'),
    ],className='slice menu')


# Applicaiton layouts
# team layout
teamLayout = html.Div([
    # While this taught me a fair amount about tables, this data will mostly be used to display Championship titles
    html.Div([dash_table.DataTable(
            id='table',
            style_as_list_view=True,
            style_table={'width': '50%','margin-left': 'auto', 'margin-right': 'auto'},
            style_header={
                    'backgroundColor': '#f8f5f0',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                },
        )],className = 'slice feature'),

    # Graphs of Historical Team statistics
    # Bar Chart of Wins and Losses
    dcc.Graph(className = 'slice feature', id='wl-bar', config={'displayModeBar': False}),
    # Line Chart of Batting Average, BABIP, and Strikeout Rate
    dcc.Graph(className = 'slice feature', id='batting-line', config={'displayModeBar': False}),
    # Line Char of Errors and Double Plays
    dcc.Graph(className = 'slice feature', id='feild-line', config={'displayModeBar': False}),
    # Line Bubble graph of K/BB ratio with ERA bubbles
    dcc.Graph(className = 'slice feature2', id='pitch-bubble', config={'displayModeBar': False}),
    # Pie Chart of % of Completed Games, Shutouts, and Saves of Total Games played
    dcc.Graph(className = 'slice feature2', id='pitch-pie', config={'displayModeBar': False}),
])

# Player layout, player data and profile
playerLayout = html.Div([
    dcc.Dropdown(
        className = 'player',
        id='player-dropdown',
        clearable=False
    ),
    dash_table.DataTable(
        id='playerProfile',
        style_as_list_view=True,
        style_header={
                'backgroundColor': '#f8f5f0',
                'fontWeight': 'bold'
            },
        style_cell={
                'textAlign': 'center',
                'padding': '8px',
            },
    ),
    dash_table.DataTable(
        id='batterTable',
        style_as_list_view=True,
        style_header={
                'backgroundColor': '#f8f5f0',
                'fontWeight': 'bold'
            },
        style_cell={
                'textAlign': 'center',
                'padding': '8px',
            },
)],className = 'slice feature app-page') # added app-page css
