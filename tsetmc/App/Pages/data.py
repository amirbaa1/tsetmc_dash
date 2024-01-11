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


df = pd.read_excel(
    r"E:\code\data_vizi\tsetmc_dash\tsetmc\App\Data\df_ektiar.xlsx")

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash.register_page(__name__, path="/data",
                   external_stylesheets=[dbc.themes.BOOTSTRAP],)

table_div = dbc.Table(
    [
        html.H1("Data tsetmc"),
        dbc.Button("Refresh", id="refresh-btn", color="primary",
                   className="me-1"), 
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
                # "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
        ),
    ]
)


layout = html.Div([table_div])


@callback(Output("table", "data"),
          Input("refresh-btn", "n_clicks")
          )
def refresh_table(n):
    if n is None:
        raise dash.exceptions.PreventUpdate
    Database.Database_Tsetmc()
    df = pd.read_excel(r"E:\code\data_vizi\tsetmc_dash\tsetmc\App\Data\df_ektiar.xlsx")
    return df.to_dict("records")

# if __name__ == "__main__":
#     run_server(debug=True)
