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

df = pd.read_excel(r"../tsetmc/df_ektiar.xlsx")


# app = dash.Dash(__name__)
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidbar_div = html.Div(
    [
        html.H2("tsetmc", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Data", href="/data", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
table_div = html.Div(
    [
        html.H1("Data tsetmc"),
        html.Button("Refresh", id="refresh-btn"),  # دکمه رفرش
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

pie_div = html.Div(
    [
        html.H4("buy pie:"),
        dcc.Graph(
            id="graph",
            style={
                "width": "80%",  # تنظیم عرض نمودار
                "height": "500px",
                "float": "right",  # تنظیم ارتفاع نمودار
            },
        ),
        html.P("status:"),
        dcc.Dropdown(
            id="status",
            options=[{"label": i, "value": i} for i in df["وضعیت"].unique()],
            value=df["وضعیت"].unique()[0],
            clearable=False,
            style={
                "width": "150px",  # تنظیم عرض Dropdown
                "height": "30px",
                "margin-left": "20%",
            },
        ),
    ]
)


content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidbar_div, content, pie_div])
# app.layout = dbc.Container(
#     [
#         my_table := dash_table.DataTable(
#             id="table",
#             columns=[{"name": i, "id": i} for i in df.columns],
#             data=df.to_dict("records"),
#             page_size=10,
#             style_data={
#                 "width": "150px",
#                 "minWidth": "150px",
#                 "maxWidth": "150px",
#                 "overflow": "hidden",
#                 "textOverflow": "ellipsis",
#             },
#         ),
#         dcc.Location(id="_pages_plugin_location"),
#     ]
# )


app.callback(Output("table", "hidden_columns"), Input("_pages_plugin_location", "href"))


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def pageNav(pathname):
    if pathname == "/":
        return html.P("HOOOOMMEEE")
    elif pathname == "/data":
        return html.Div(table_div)


@app.callback(Output("table", "data"), [Input("refresh-btn", "n_clicks")])
def refresh_table(n):
    if n is None:
        raise dash.exceptions.PreventUpdate
    Database.Database_Tsetmc()
    df = pd.read_excel(r"../tsetmc/df_ektiar.xlsx")
    return df.to_dict("records")


@app.callback(Output("graph", "figure"), Input("status", "value"))
def generate_chart(status):
    filtered_df = df[df["وضعیت"] == status]
    fig = px.pie(data_frame=filtered_df, names="نام نماد", hole=0.3)
    return fig


# @app.callback(Output("time_refresh", "children"), [Input("refresh-btn", "n_clicks")])
# def update_last_refresh(update):
#     if update is None:
#         raise dash.exceptions.PreventUpdate
#     return f"Last Refresh Time: {datetime.now()}" #delete please !


if __name__ == "__main__":
    app.run_server(debug=True)
