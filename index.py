# import dash-core, dash-html, dash io, bootstrap
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks
from layouts import appMenu, menuSlider, playerMenu, teamLayout, battingLayout, fieldingLayout
import callbacks

# Import app
from app import app
# Import server for deployment
from app import srv as server

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
        html.H2("Major League Baseball", className="display-5"),
        html.H2("Data Explorer", className="display-5"),
        html.Hr(),
        html.H2("Historical Analysis", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Team Analysis", href="/team", active="exact"),
                dbc.NavLink("Batting Analysis", href="/player", active="exact"),
                dbc.NavLink("Pitching/Feilding Analysis", href="/field", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.H2("Machine Learning Analysis", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Linear Analysis", href="/mline", active="exact"),
                # dbc.NavLink("Batting Analysis", href="/player", active="exact"),
                # dbc.NavLink("Pitching/Feilding Analysis", href="/field", active="exact"),
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
            ### The Applicaiton
            This application is a portfolio project built by [Matt Parra](https://devparra.github.io/) using Plotly's Dash,
            faculty.ai's Dash Bootstrap Components, and Pandas. Using historical MLB (Major League Baseball) data,
            this application provides visualizations for team and player statistics dating from 1903 to 2020. Selecting
            from a dropdown menu, the era will update the list of available teams and players in the range set on the years
            slider. The slider allows the user to adjust the range of years with which the data is presented.

            ### The Analysis
            The applicaiton breaks down each baseballs teams win/loss performance within a range of the teams history.
            Additionally, the application will break down the batting performance with the team batting average, BABIP, and strikeout
            rate. The application also brakes down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding
            performance of each team is illustrated with total errors and double plays. The applicaiton will also breakdown
            each of teams players statistics within the given era.

            ### The Data
            The data used in this application was retrieved from [Seanlahman.com](http://www.seanlahman.com/baseball-archive/statistics/).
            Provided by [Chadwick Baseball Bureau's GitHub](https://github.com/chadwickbureau/baseballdatabank/) .
            This database is copyright 1996-2021 by Sean Lahman. This data is licensed under a Creative Commons Attribution-ShareAlike
            3.0 Unported License. For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)
        ''')],className='home')
    elif pathname == '/team':
        return appMenu, menuSlider, teamLayout
    elif pathname == '/player':
        return appMenu, menuSlider, playerMenu, battingLayout
    elif pathname == '/field':
        return appMenu, menuSlider, playerMenu, fieldingLayout
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
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
