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

# df = pd.read_excel(
#     r"\\tsetmc\App\\Data\df_ektiar.xlsx")

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "..", "Data", "df_ektiar.xlsx")

df = pd.read_excel(file_path)

dash.register_page(__name__, path="/")

pie_div = html.Div(
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="graph",
                ),
            ],

        ),

    )
)


pie_fig_2 = html.Div(
    dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id="pie_fig_2",
                ),

            ],

        ),

    )
)


pie_div_buy_sell = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(
                id="graph_pie_buy_sell",

            )
        ]
    ),
    # style={"maxWidth": 600, "text-align": "right", }
)


bar_fig = dbc.Card(
    dbc.CardBody(
        dcc.Graph(
            id="bar_fig",
        )
    )
)


def namad_high_dropdown(df):
    sum_df = df.groupby('دسته')['مقدار'].sum().reset_index()
    sum_df_sorted = sum_df.sort_values(by="مقدار", ascending=False)
    top_categories = sum_df_sorted['دسته'].head(6).tolist()
    return top_categories


sidebar = html.Div(
    [
        html.P('Sidebar'),
        dcc.Dropdown(
            id="symbols",
            options=[{'label': i, 'value': i}
                     for i in df['دسته'].unique()],
            value=namad_high_dropdown(df),
            multi=True,
            style={"width": "100%", "margin-bottom": "20px"},
        ),
        dcc.Dropdown(
            id="status",
            options=[{"label": i, "value": i}
                     for i in df["وضعیت"].unique()],
            value=df["وضعیت"].unique()[0],
            clearable=False,
            style={"width": "100%", "margin-bottom": "20px"},
        ),
        dcc.Dropdown(
            id="selector",
            options=[
                {'label': 'معامله', 'value': 'معامله'},
                {'label': 'مقدار', 'value': 'مقدار'}
            ],
            value='معامله',
            style={"width": "100%", "margin-bottom": "20px"},
        ),

        dbc.Row(
            [
                html.Div([
                    html.P('Target Variables',
                           className='font-weight-bold'),
                    pie_div_buy_sell
                ])
            ],
            style={"height": "45vh", 'margin': '8px'}
        )

    ]
)

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        pie_div
                    ],
                    className='bg-light'
                ),
                dbc.Col(
                    [
                        # pie_div_buy_sell
                        pie_fig_2
                    ],
                    className='bg-light'
                )
            ],
            style={'height': '50vh',
                   'margin-top': '16px', 'margin-left': '8px',
                   'margin-bottom': '8px', 'margin-right': '8px'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        bar_fig
                    ],
                    className='bg-light'
                )
            ],
            style={"height": "50vh", 'margin': '8px'}
        )
    ]
)

home = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9, class_name="mx-auto")
            ],
            style={"height": "100vh"}
        ),
    ],
    fluid=True
)


layout = html.Div([home, dcc.Interval(
    id='interval-component',
    interval=60 * 1000,  # میلی‌ثانیه
    n_intervals=0
),html.Div(id='table')])

# pig namad and status and sum namad


def generate_pie_chart(selected_status, selected_symbols):
    if not isinstance(selected_symbols, list):
        selected_symbols = [selected_symbols]

    filtered_df = df[(df["وضعیت"] == selected_status) &
                     (df["دسته"].isin(selected_symbols))]

    fig = px.pie(data_frame=filtered_df, names="دسته", hole=0.6)
    fig.update_layout(
        title='خرید و فروش تعداد نماد ها',
        title_font=dict(size=20)
    )
    return fig

# pig namad and status and sum namad


@callback(
    Output("graph", "figure"),
    [Input("status", "value"),
     Input("symbols", "value")]
)
def update_pie_chart(selected_status, selected_symbols):
    return generate_pie_chart(selected_status, selected_symbols)


# pie2 namad megdar v mamaele
@callback(
    Output("pie_fig_2", "figure"),
    [Input("symbols", "value"),
     Input("selector", "value")]
)
def generate_pie_2_chart(selected_symbols, selector):
    if not isinstance(selected_symbols, list):
        selected_symbols = [selected_symbols]

    bar_df = df[(df["دسته"].isin(selected_symbols))]
    # grouped_df_sum = bar_df.groupby(['وضعیت', 'دسته']).agg(
    #     {"مقدار": "sum"}).reset_index()

    grouped_df_sum = bar_df.groupby(['وضعیت', 'دسته']).agg(
        {"مقدار": "mean"}).reset_index()

    grouped_df_transaction = bar_df.groupby(['وضعیت', 'دسته']).agg(
        {"معامله": "sum"}).reset_index()

    if selector == 'مقدار':
        # fig = px.pie(data_frame=grouped_df_sum, names='دسته', hole=0.6)
        fig = px.pie(data_frame=grouped_df_sum, names='دسته',
                     values='مقدار', custom_data=['مقدار'], hole=0.6)

        fig.update_layout(
            title='مقدار نماد ها',
            title_font=dict(size=20)
        )
        return fig

    elif selector == 'معامله':
        # fig = px.pie(data_frame=grouped_df_transaction, names='دسته', hole=0.6)
        fig = px.pie(data_frame=grouped_df_transaction, names='دسته',
                     values='معامله', custom_data=['معامله'], hole=0.6)

        fig.update_layout(
            title='معامله نماد ها',
            title_font=dict(size=20)
        )
        return fig


# pig sell and buy


@callback(
    Output('graph_pie_buy_sell', 'figure'),
    Input('graph_pie_buy_sell', 'id')
)
def generate_chart_buy_sell(id):
    count_values = df['وضعیت'].value_counts()
    buy_count = count_values.get('خرید', 0)
    sell_count = count_values.get('فروش', 0)

    labels = ['خرید', 'فروش']
    pie_fig = px.pie(names=labels, values=[buy_count, sell_count], hole=0.6)

    pie_fig.update_layout(
        title='تعداد خرید و فروش امروز',
        title_font=dict(size=20)
    )

    return pie_fig

# bar fig


@callback(
    Output("bar_fig", "figure"),
    [Input("symbols", "value"),
     Input("selector", "value")]
)
def bar_chart(selected_symbols, selector):
    if not isinstance(selected_symbols, list):
        selected_symbols = [selected_symbols]

    bar_df = df[(df["دسته"].isin(selected_symbols))]
    grouped_df_sum = bar_df.groupby(['وضعیت', 'دسته']).agg(
        {"مقدار": "sum"}).reset_index()

    grouped_df_transaction = bar_df.groupby(['وضعیت', 'دسته']).agg(
        {"معامله": "sum"}).reset_index()

    if selector == 'مقدار':
        fig = px.bar(data_frame=grouped_df_sum, x='دسته',
                     y="مقدار", color="وضعیت", barmode="group")
        fig.update_layout(
            title='خرید و فروش مقدار نماد ها',
            title_font=dict(size=20)
        )
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        return fig

    elif selector == 'معامله':
        fig = px.bar(data_frame=grouped_df_transaction, x='دسته',
                     y="معامله", color="وضعیت", barmode="group")
        fig.update_layout(
            title='خرید و فروش نماد ها',
            title_font=dict(size=20)
        )
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        return fig


# @callback(Output("table", "children"),
#           Input("interval-component", "n_intervals")
#           )
# def refresh_table(n_intervals):
#     print("Callback is running...")
#     Database.Database_Tsetmc()
#     directory = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(directory, "..", "Data", "df_ektiar.xlsx")

#     df = pd.read_excel(file_path)

#     # df = pd.read_excel(r"...\tsetmc\app\Data\df_ektiar.xlsx")
#     return df.to_dict("records")
