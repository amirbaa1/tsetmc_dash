import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    pages_folder="pages",
    use_pages=True
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.Col(
            children=[
                dbc.Button(dbc.NavItem(dbc.NavLink("Data", href="/data")))
            ],
        ),

    ],
    brand="Tsetmc",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [navbar, dash.page_container]
)

if __name__ == '__main__':
    app.run_server(debug=True)
