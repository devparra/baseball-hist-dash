# Import Bootstrap from Dash
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
                    dbc.DropdownMenuItem("Player Analysis", href='/player'),
                ],
            ),
        ],
        brand="Home",
        brand_href="/",
        sticky="top",
        color="light",
        dark=False,)
    return navbar
