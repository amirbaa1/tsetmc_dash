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
            # dbc.Button(
            #     "Data", color="primary", className="ms-2", n_clicks=0, href="/data/"
            # ),
            # width="auto",
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
# lol = html.Div([
#     html.H1('Multi-page app with Dash Pages'),
#     html.Div([
#         html.Div(
#             dcc.Link(f"{page['name']}",
#                      href=page["relative_path"])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])
### DELEETE
# lol = html.Div([
#     html.Div([
#         html.Div(
#             # dcc.Link(f"{page['name']}",
#             #          href=page["relative_path"])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])

app.layout = html.Div(
    [navbar, dash.page_container]
)

if __name__ == '__main__':
    app.run_server(debug=True)
