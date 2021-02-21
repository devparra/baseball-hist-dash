# Import Bootstrap components
import dash_bootstrap_components as dbc


# Navigation Bar fucntion
def Navbar():
    navbar = dbc.NavbarSimple(children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="MENU",
            children=[
                    dbc.DropdownMenuItem("Team Analysis", href='/team'),
                    dbc.DropdownMenuItem("Batting Analysis", href='/batter'),
                    dbc.DropdownMenuItem("Pitching/Fielding Analysis", href='/field'),
                ],
            ),
        ],
        brand="Home",
        brand_href="/",
        sticky="top",
        color="light",
        dark=False,)
    return navbar
