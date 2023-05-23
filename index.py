# import dash-core, dash-html, dash io, bootstrap
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# layouts and custom callbacks
from layouts import teamLayout, teamVLayout, rosterLayout, regLayout
from historical import team_analysis, team_v_analysis, roster_analysis
from player import ml_analytics

# Import app
from app import app
# Import server for deployment
# from app import srv as server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Major League Baseball", className="display-6"),
        html.H2("Data Explorer", className="display-8"),
        html.Hr(),
        dbc.Nav(
            [dbc.NavLink("Home", href="/", active="exact")],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Team Analysis", href="/team", active="exact"),
                dbc.NavLink("Roster Analysis", href="/roster", active="exact"),
                dbc.NavLink("Team V. Team", href="/teamvteam", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Regression Analysis", href="/regression", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# Sidebar layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return html.Div([dcc.Markdown('''
            ### Introduction
            This application is a portfolio project built by [Matthew Parra](https://devparra.github.io/) using Plotly's Dash,
            faculty.ai's Dash Bootstrap Components, Pandas, and custom functions. Using historical MLB (Major League Baseball) data, 
            this application provides visualizations for team and player statistics dating from 1871 to 2022. This application also 
            provides player projections and regression analysis.

            The data used in this application was retrieved from [Seanlahman.com](http://seanlahman.com/download-baseball-database/).
            Provided by [Nat Dunn's WebucatorTraining](https://github.com/WebucatorTraining/lahman-baseball-mysql). Database was updated with 
            data provided by [Chadwick Baseball Bureau](https://github.com/chadwickbureau/baseballdatabank/).
            The data is copyright 1996-2023 by Sean Lahman. Licensed under a Creative Commons Attribution-ShareAlike
            3.0 Unported License. For details see: [CreativeCommons v3](http://creativecommons.org/licenses/by-sa/3.0/).
            SQL database is licensed under the Creative Commons Zero v1.0 Universal License. 
            For details see: [CreativeCommons v1](https://creativecommons.org/publicdomain/zero/1.0/).
        ''')],className='home')
    elif pathname == '/team':
        return teamLayout
    elif pathname == '/teamvteam':
        return teamVLayout
    elif pathname == '/roster':
        return rosterLayout
    elif pathname == '/regression':
        return regLayout
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Card(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

# Call app server
if __name__ == '__main__':
    # set debug to false when deploying app
    app.run_server(debug=True)