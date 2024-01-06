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
    r"E:\code\data_vizi\tsetmc_dash\tsetmc\df_ektiar.xlsx")

dash.register_page(__name__, path="/")

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
grouped_df = df.groupby('نام نماد')['مقدار'].mean().reset_index()


# ساخت Bubble Chart با plotly.express
fig = px.scatter(grouped_df, x='مقدار', y=grouped_df.index, text='نام نماد', size_max=600, log_x=True)

# fig.update_traces(marker=dict(size=10))

fig.update_layout(title='Bubble Chart', showlegend=False)
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


layout = html.Div([
    html.H1('HOOOOME'), combined_div, dcc.Graph(figure=fig)
])


@callback(Output("graph", "figure"), Input("status", "value"))
def generate_chart(status):
    filtered_df = df[df["وضعیت"] == status]
    fig = px.pie(data_frame=filtered_df, names="نام نماد", hole=0.1)
    return fig


@callback(
    Output('graph_pie_buy_sell', 'figure'),
    Input('graph_pie_buy_sell', 'id')
)
def generate_chart_buy_sell(id):
    count_values = df['وضعیت'].value_counts()
    buy_count = count_values.get('خرید', 0)
    sell_count = count_values.get('فروش', 0)

    labels = ['خرید', 'فروش']
    return px.pie(names=labels, values=[buy_count, sell_count], hole=0.1)
