import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dash_table
from datadb import Database
from datetime import datetime
import plotly.express as px


df = pd.read_excel(
    r"E:\code\data_vizi\tsetmc_dash\tsetmc\df_ektiar.xlsx")

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.Col(
            dbc.Button(
                "Data", color="primary", className="ms-2", n_clicks=0,href="/data/"
            ),
            width="auto",
        ),
    ],
    brand="Tsetmc",
    brand_href="#",
    color="dark",
    dark=True,
)

cards = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Custom CSS", className="card-title"),
            html.P(
                "This card has inline styles applied controlling the width. "
                "You could also apply the same styles with a custom CSS class."
            ),
        ]
    ),
    style={"width": "18rem"},
)


table_div = dbc.Table(
    [
        html.H1("Data tsetmc"),
        dbc.Button("Refresh", id="refresh-btn", color="primary",
                   className="me-1"),  # دکمه رفرش
        html.Div(id="log-output"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            page_size=36,
            style_data={
                "width": "150px",
                "minWidth": "150px",
                "maxWidth": "150px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
        ),
    ]
)

app.layout = html.Div(
    [navbar, cards, table_div]
)


@app.callback(Output("table", "data"), [Input("refresh-btn", "n_clicks")])
def refresh_table(n):
    if n is None:
        raise dash.exceptions.PreventUpdate
    Database.Database_Tsetmc()
    df = pd.read_excel(r"E:\code\data_vizi\tsetmc_dash\tsetmc\df_ektiar.xlsx")
    return df.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
