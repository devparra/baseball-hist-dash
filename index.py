# import dash-core, dash-html, dash io, bootstrap
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks
from navbar import Navbar
from layouts import appMenu, menuSlider, playerMenu, teamLayout, battingLayout, fieldingLayout
import callbacks

# Instantiate app with dash
from app import app


# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div([
            html.H2(children='Major League Baseball History'),
            html.H3(children='A Visualization of Historical Data')])
        ),className='banner')

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
    The data used in this application was retrieved from Kaggle and was created by code at
    [Benhamner's GitHub](https://github.com/benhamner/baseball). It is a processed version
    of the 2015 data at [Seanlahman.com](http://www.seanlahman.com/baseball-archive/statistics/).
    The original database was copyright 1996-2015 by Sean Lahman and licensed under a
    Creative Commons Attribution-ShareAlike 3.0 Unported License.
    For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
    '''),])


# Menu callback, set and return
# Declair function  that connects other pages with content to container
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([dcc.Markdown('''
            ### The Applicaiton
            This application is a portfolio project built using Plotly's Dash, Dash Bootstrap Components, and Pandas.
            Using historical MLB (Major League Baseball) data, this application provides visualizations for team and player
            statistics dating from 1903 to 2015. Selecting from a dropdown menu, the era will update the list of available
            teams and players in the range set on the years slider. The slider allows the user to adjust the range of years
            with wich the data is presented.

            ### The Analysis
            The applicaiton breaks down each baseballs teams win/loss performance within a range of the teams history.
            Additionally, the app will break down the batting performance with the team batting average, BABIP, and strikeout
            rate. I also broke down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding
            performance of each team is illustrated with total errors and double plays. The applicaiton will also breakdown
            each of teams players statistics within the given era.

        ''')],style={'height': '700px','padding': '5%'})
    elif pathname == '/team':
        return appMenu, menuSlider, teamLayout
    elif pathname == '/batter':
        return appMenu, menuSlider, playerMenu, battingLayout
    elif pathname == '/field':
        return appMenu, menuSlider, playerMenu, fieldingLayout
    else:
        return 'ERROR 404: Page not found!'


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([
            nav,
            container,
            footer
        ])
    return layout

# Set layout to index function
app.layout = index()

# Call app server
if __name__ == '__main__':
    app.run_server(debug=True)
