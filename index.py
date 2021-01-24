# import dash-core, dash-html, dash io, bootstrap
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# Import Pandas
import pandas as pd

# import Navbar, layouts, callbacks
from navbar import Navbar
from layouts import appMenu, teamLayout, playerLayout
import callbacks

# Import app
from app import app


# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div([
            html.H1(children='Major League Baseball History'),
            html.H2(children='A Visualization of Historical Data')])
        ),
    className='banner')

content = html.Div([
    dcc.Location(id='url'),
    html.Div(id='page-content')
])

container = dbc.Container([
    header,
    content,
])

# Footer with acknowledments
footer = html.Footer([dcc.Markdown('''
    The data used in this app was retrieved from Kaggle and was created by code at
    [Benhamner's GitHub](https://github.com/benhamner/baseball). It is a processed version
    of the 2015 data at [Seanlahman.com](http://www.seanlahman.com/baseball-archive/statistics/).
    The original database was copyright 1996-2015 by Sean Lahman and licensed under a
    Creative Commons Attribution-ShareAlike 3.0 Unported License.
    For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
    '''),])


# main menu callback
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([dcc.Markdown('''
            ### The Applicaiton
            This application is a portfolio project built using Plotly's Dash, Dash Bootstrap Components, Pandas, and Numpy.
            Taking historical MLB (Major League Baseball) data, this application provides visualizations for teams and player
            statistics dating from 1903 to 2015. Selecting from a dropdown menu, the era will update the list of available
            teams and players in the range set on the years slider. The slider allows the user to adjust the range of years
            with wich the data shows.

            ### The Analysis
            The applicaiton breaks down each baseballs teams win/loss performance within a range of the teams history.
            Additionally, the app will break down the batting performance with the team batting average, BABIP, and strikeout
            rate. I also broke down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding
            performance of each team is illustrated with total errors and double plays. \*The applicaiton will also breakdown
            each of teams players statistics within the given era.

            \* *Applicaiton feature is recently added and still under construction*
        ''')],className='home')
    elif pathname == '/team':
        return appMenu, teamLayout
    elif pathname == '/player':
        return appMenu, playerLayout
    else:
        return 'ERROR 404: Page not found!'


# main index function that will call all elements
def index():
    layout = html.Div([
            nav,
            container,
            footer
        ])
    return layout

# set layout to index function
app.layout = index()

# call app server
if __name__ == '__main__':
    app.run_server(debug=True)
