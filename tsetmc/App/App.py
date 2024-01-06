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

# df = pd.read_excel(r"../tsetmc/df_ektiar.xlsx") for macOS
df = pd.read_excel(
    r"E:\code\data_vizi\tsetmc_dash\tsetmc\df_ektiar.xlsx")  # for win

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
    "width": "14rem",
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

pie_div = html.Div(
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="graph",
                    # style={
                    #     "width": "80%",  # تنظیم عرض نمودار
                    #     "height": "500px",
                    #     "float": "right",  # تنظیم ارتفاع نمودار
                    # },
                ),
                # html.P("status:"),
                dcc.Dropdown(
                    id="status",
                    options=[{"label": i, "value": i}
                             for i in df["وضعیت"].unique()],
                    value=df["وضعیت"].unique()[0],
                    clearable=False,
                    # style={
                    #     "width": "150px",  # تنظیم عرض Dropdown
                    #     "height": "30px",
                    #     "float": "right",
                    #     "margin-right": "20%",
                    # },
                ),
            ],
            # style={"clear": "both"}
        ),
        class_name="shadow",
        style={"maxWidth": 500, "text-align": "center", }
    )
)

pie_div_buy_sell = dbc.Card(
    dbc.CardBody(
        [
            html.H4("خرید و فروش", className="card-title"),
            dcc.Graph(
                id="graph_pie_buy_sell",
                style={
                    #     "width": "80%",
                    "height": "480px",
                    #     "float": "right",
                    #     "text-align": "center"
                }
            )
        ]
    ),
    class_name="shadow",
    # style={"maxWidth": 600, "text-align": "right", }
)


combined_div = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(pie_div, width=3, className="mx-auto text-center"),
                dbc.Col(pie_div_buy_sell, width=3,
                        className="mx-auto text-center"),
            ]
        )
    ]
)


content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"),
                       dcc.Location(id="data-url"), sidbar_div,
                       content])
# app.layout = html.Div([dcc.Location(id="Data"),])
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

data_layout = html.Div([
    dcc.Location(id="data-url"),
    table_div
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"), Input("data-url", "pathname")]
)
def display_page(pathname, data_pathname):
    if pathname == "/":
        return combined_div
    elif data_pathname == "/data":
        return data_layout


@app.callback(Output("table", "data"), [Input("refresh-btn", "n_clicks")])
def refresh_table(n):
    if n is None:
        raise dash.exceptions.PreventUpdate
    Database.Database_Tsetmc()
    df = pd.read_excel(r"E:\code\data_vizi\tsetmc_dash\tsetmc\df_ektiar.xlsx")
    return df.to_dict("records")


@app.callback(Output("graph", "figure"), Input("status", "value"))
def generate_chart(status):
    filtered_df = df[df["وضعیت"] == status]
    fig = px.pie(data_frame=filtered_df, names="نام نماد", hole=0.1)
    return fig


@app.callback(
    Output('graph_pie_buy_sell', 'figure'),
    Input('graph_pie_buy_sell', 'id')
)
def generate_chart_buy_sell(id):
    count_values = df['وضعیت'].value_counts()
    buy_count = count_values.get('خرید', 0)
    sell_count = count_values.get('فروش', 0)

    labels = ['خرید', 'فروش']
    return px.pie(names=labels, values=[buy_count, sell_count], hole=0.1)


# @app.callback(
#     Output('graph_pie_buy_sell', 'figure'),
#     Input('graph_pie_buy_sell', 'id')
# )
# def update_pie_chart(id):
#     return generate_chart_buy_sell()


if __name__ == "__main__":
    app.run_server(debug=True)
