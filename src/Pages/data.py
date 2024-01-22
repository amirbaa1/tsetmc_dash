import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dash_table

# from datadb import Database
from Services.datadb import Database
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import os
from datetime import datetime, timedelta

# df = pd.read_excel(
#     r"\\tsetmc\App\Data\df_ektiar.xlsx")


directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(directory, "..", "Data", "df_ektiar.xlsx")

df = pd.read_excel(file_path)

dash.register_page(
    __name__,
    path="/data",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

table_div = dbc.Table(
    [
        html.H1("Data tsetmc"),
        # dbc.Button("Refresh", id="refresh-btn", color="primary",
        #            className="me-1"),
        html.Div(id="log-output"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": str(i), "id": str(i)} for i in df.columns],
            data=df.to_dict("records"),
            page_size=36,
            style_data={
                "width": "150px",
                "minWidth": "150px",
                "maxWidth": "150px",
                # "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
        ),
    ]
)


layout = html.Div(
    [
        table_div,
        dcc.Interval(id="interval-component",
                     interval=35 * 1000, n_intervals=0),
    ]
)

# refresh
# @callback(Output("table", "data"),
#           [Input("refresh-btn", "n_clicks"),
#            Input("interval-component", "n_intervals")]
#           )
# def refresh_table(n_intervals, n):
#     if n is None:
#         raise dash.exceptions.PreventUpdate
#     Database.Database_Tsetmc()
#     directory = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(directory, "..", "Data", "df_ektiar.xlsx")

#     df = pd.read_excel(file_path)

#     # df = pd.read_excel(r"...\tsetmc\app\Data\df_ektiar.xlsx")
#     return df.to_dict("records")


@callback(Output("table", "data"),
          Input("interval-component", "n_intervals"))
def refresh_table(n_intervals):
    Database.Database_Tsetmc()
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, "..", "Data", "df_ektiar.xlsx")

    df = pd.read_excel(file_path)

    # df = pd.read_excel(r"...\tsetmc\app\Data\df_ektiar.xlsx")
    return df.to_dict("records")


# if __name__ == "__main__":
#     run_server(debug=True)
