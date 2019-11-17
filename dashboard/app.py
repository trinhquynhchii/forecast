# -*- coding: utf-8 -*-
import argparse
import datetime as dt
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_table
from plotly.subplots import make_subplots

from dashboard.data_manager import DashboardDataManager
from dashboard.utils import clean_safety_stock_df
from dashboard.config import DATA_DIR, REPORT_DIR

pd.options.display.float_format = '${:,.2f}'.format

data = DashboardDataManager(data_dir=DATA_DIR,
                            report_dir=REPORT_DIR,
                            data_file_name='fake_data.csv',
                            pre_forecasted=True)
# data.data_manager.df['Kho'] = data.data_manager.df['Kho'].apply(lambda x: x.)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    className="row",
    children=[
        # Left Panel Div
        # html.Div(
        #     className="three columns",
        #     # className="three columns div-left-panel",
        #     # className="three columns pretty_container",
        #     children=[
        #         # Div for Left Panel App Info
        #         html.Div(
        #             children=[
        #                 html.H3(
        #                     'Diaper Project',
        #                     style={"margin-top": "0px"},
        #                 ),
        #                 html.P(
        #                     # """
        #                     # This app continually queries csv files and updates Ask and Bid prices
        #                     # for major currency pairs as well as Stock Charts. You can also virtually
        #                     # buy and sell stocks and see the profit updates.
        #                     # """
        #                     """
        #                     Add description here
        #                     """
        #                 ),
        #             ],
        #             className="pretty_container",
        #         ),
        #         # TODO: percentage sku
        #         # html.Div(
        #         #     className="div-currency-toggles",
        #         #     children=[
        #         #         html.P(
        #         #             id="live_clock",
        #         #             className="three-col",
        #         #             children=datetime.datetime.now().strftime("%H:%M:%S"),
        #         #         ),
        #         #         html.P(className="three-col", children="Bid"),
        #         #         html.P(className="three-col", children="Ask"),
        #         #         html.Div(
        #         #             id="pairs",
        #         #             className="div-bid-ask",
        #         #             children=[
        #         #                 get_row(first_ask_bid(pair, datetime.datetime.now()))
        #         #                 for pair in currencies
        #         #             ],
        #         #         ),
        #         #     ],
        #         # ),
        #         html.Div(
        #             children=[
        #                 html.P(
        #                     """
        #                     Choose warehouse:
        #                     """
        #                 ),
        #                 html.Div(
        #                     # className="display-inlineblock",
        #                     children=[
        #                         dcc.Dropdown(
        #                             id="dropdown_warehouses",
        #                             className="bottom-dropdown",
        #                             options=[
        #                                 {"label": "Hà Nội", "value": "Hà Nội"},
        #                                 {"label": "Đà Nẵng", "value": "Đà Nẵng"},
        #                                 {"label": "Bình Dương", "value": "Bình Dương"},
        #                             ],
        #                             value="Hà Nội",
        #                             clearable=False,
        #                             style={"border": "0px solid black"},
        #                         )
        #                     ],
        #                 ),
        #                 html.P(
        #                     """
        #                     Choose forecast period:
        #                     """
        #                 ),
        #                 html.Div(
        #                     # className="display-inlineblock float-right",
        #                     children=[
        #                         html.Div(
        #                             id="period_menu",
        #                             children=[
        #                                 dcc.Dropdown(
        #                                     className="bottom-dropdown",
        #                                     id="period_range",
        #                                     options=[
        #                                         # {"label": "1 day", "value": "1", },
        #                                         {"label": "7 days", "value": "7"},
        #                                         {"label": "14 days", "value": "14"},
        #                                         {"label": "30 days", "value": "30"},
        #                                     ],
        #                                     value="7",
        #                                     clearable=False,
        #                                     style={"border": "0px solid black"},
        #                                 )
        #                             ],
        #                         ),
        #                     ],
        #                 ),
        #                 html.P(
        #                     """
        #                     Choose date to compute safety stock:
        #                     """
        #                 ),
        #                 dcc.DatePickerRange(
        #                     id='date_picker_range',
        #                     display_format='D/M/YYYY',
        #                     min_date_allowed=data.get_min_date(),
        #                     max_date_allowed=data.get_max_date() + dt.timedelta(days=1),
        #                     initial_visible_month=dt.date.today(),
        #                     start_date=data.get_max_date() - dt.timedelta(days=14),
        #                     end_date=data.get_max_date(),
        #                     className="dcc_control",
        #                 ),
        #             ],
        #             className="pretty_container",
        #         ),
        #         html.Div(id="predict_percentage_table", className="row pretty_container"),
        #     ],
        # ),
        # Right Panel Div
        html.Div(
            # className="nine columns",
            children=[
                html.Div(
                    children=[
                        html.H3(
                            'Diaper Project',
                        ),
                    ],
                    style={'text-align': 'center'},
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.P(
                                    """
                                    Choose warehouse:
                                    """
                                ),
                                html.Div(
                                    # className="display-inlineblock",
                                    children=[
                                        dcc.Dropdown(
                                            id="dropdown_warehouses",
                                            className="bottom-dropdown",
                                            options=[
                                                {"label": "Hà Nội", "value": "Hà Nội"},
                                                {"label": "Đà Nẵng", "value": "Đà Nẵng"},
                                                {"label": "Bình Dương", "value": "Bình Dương"},
                                            ],
                                            value="Hà Nội",
                                            clearable=False,
                                            style={"border": "0px solid black"},
                                        )
                                    ],
                                ),
                            ],
                            className="three columns"
                        ),
                        html.Div(
                            children=[
                                html.P(
                                    """
                                    Choose forecast period:
                                    """
                                ),
                                html.Div(
                                    # className="display-inlineblock float-right",
                                    children=[
                                        html.Div(
                                            id="period_menu",
                                            children=[
                                                dcc.Dropdown(
                                                    className="bottom-dropdown",
                                                    id="period_range",
                                                    options=[
                                                        # {"label": "1 day", "value": "1", },
                                                        {"label": "7 days", "value": "7"},
                                                        {"label": "14 days", "value": "14"},
                                                        {"label": "30 days", "value": "30"},
                                                    ],
                                                    value="7",
                                                    clearable=False,
                                                    style={"border": "0px solid black"},
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                            className="three columns"
                        ),
                        html.Div(
                            children=[
                                html.P(
                                    """
                                    Choose date to compute safety stock:
                                    """
                                ),
                                dcc.DatePickerRange(
                                    id='date_picker_range',
                                    display_format='D/M/YYYY',
                                    min_date_allowed=data.get_min_date(),
                                    max_date_allowed=data.get_max_date() + dt.timedelta(days=1),
                                    initial_visible_month=dt.date.today(),
                                    start_date=data.get_max_date() - dt.timedelta(days=14),
                                    end_date=data.get_max_date(),
                                    className="dcc_control",
                                ),
                            ],
                            className="four columns"
                        ),
                    ],
                    className="pretty_container row",
                ),
                #     ],
                html.Div(
                    id="charts",
                    className="row",
                    children=[html.Div(
                        id="prediction_plot",
                        className="pretty_container",
                        children=[
                            html.Div(
                                children=[
                                    html.H6(
                                        'Prediction plot',
                                    ),
                                ],
                                style={'text-align': 'center'},
                            ),
                            # html.Div(
                            #     className="row chart-top-bar",
                            #     children=[
                            #         html.Span(
                            #             id="time_button",
                            #             className="inline-block chart-title",
                            #             children="Time period ☰",
                            #             n_clicks=0,
                            #         ),
                            #     ],
                            # ),
                            # Graph div
                            html.Div(
                                dcc.Graph(
                                    id="prediction_chart",
                                    className="chart-graph",
                                    config={"displayModeBar": False, "scrollZoom": True},
                                )
                            ),
                        ],
                    )],
                ),

                # html.Div(
                #     id="top_bar",
                #     className="row div-top-bar",
                #     children=[],
                # ),
                html.Div(
                    id="bottom_panel",
                    className="row pretty_container",
                    children=[
                        html.Div(
                            children=[
                                html.H6(
                                    'Safety Stock',
                                ),
                            ],
                            style={'text-align': 'center'},
                        ),
                        html.Div(
                            className="display-inlineblock",
                            children=[
                                # dcc.Dropdown(
                                #     id="closable_orders",
                                #     className="bottom-dropdown",
                                #     placeholder="Close order",
                                # )
                            ],
                        ),
                        dcc.Loading(
                            id="loading",
                            children=[
                                html.Div(id="safety_stock_table", className="row safety_stock_table"),
                            ],
                            type="circle",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# updates hidden div with all the clicked charts
@app.callback(
    Output("prediction_chart", "figure"),
    [Input("period_range", "value"),
     Input("dropdown_warehouses", "value")],
    # [State("charts_clicked", "children")],
)
def get_fig(period, warehouse):
    # Get forecast data
    period = int(period)
    df = data.df_by_day
    forecast, conf_int = data.forecast(warehouse, period)

    fig = make_subplots(
        rows=1,
        shared_xaxes=True,
        shared_yaxes=True,
        cols=1,
        print_grid=False,
        vertical_spacing=0.12,
    )

    index_of_fc = []
    for day in range(period):
        time_shift = pd.to_timedelta(day + 1, unit='D')
        index_of_fc.append(df.index[-1] + time_shift)

    fc_series = pd.Series(forecast, index=index_of_fc)
    lower_series = pd.Series(conf_int[:, 0], index=index_of_fc)
    upper_series = pd.Series(conf_int[:, 1], index=index_of_fc)

    fig.add_trace(go.Scatter(
        x=upper_series.index, y=upper_series, mode='none', showlegend=False, fill='tonexty',
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=lower_series.index, y=lower_series, mode='none', showlegend=False,
        hoverinfo='skip'
    ))

    idx_last_90_days = df.index[-1] + pd.to_timedelta(-90, unit='D')
    df = df[idx_last_90_days:]
    fig.add_trace(go.Scatter(
        x=df.index, y=df[warehouse], mode="lines", showlegend=False, name="Actual Sale",
        hovertemplate='Quantity: %{y}<br>' +
                      'Date: %{text}<extra></extra>',
        text=df.index.strftime('%d/%m/%Y'),
    ))
    fig.add_trace(go.Scatter(
        x=fc_series.index, y=fc_series, mode='lines', showlegend=False, name="Prediction",
        hovertemplate='Quantity: %{y}<br>' +
                      'Date: %{text}<extra></extra>',
        text=fc_series.index.strftime('%d/%m/%Y'),
    ))

    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["hoverlabel"]["namelength"] = 0
    # fig["layout"]["xaxis"]["tickformat"] = "%"
    # fig["layout"]["xaxis"]["showgrid"] = False
    # fig["layout"]["yaxis"]["showgrid"] = True
    # fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    # fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"].update(paper_bgcolor="#F9F9F9", plot_bgcolor="#F9F9F9")

    return fig


@app.callback(
    Output("safety_stock_table", "children"),
    [Input("dropdown_warehouses", "value"),
     Input("period_range", "value"),
     Input("date_picker_range", "start_date"),
     Input("date_picker_range", "end_date"), ]
)
# def get_safety_stock_table(warehouse, start_date, end_date):
#     df = data.calculate_safety_stock((start_date, end_date))
#     warehouse = f'Kho {warehouse}'
#     df = df.loc[df['Kho'] == warehouse, :].drop('Kho', axis=1)
#
#     def df_to_table(df):
#         return html.Table(
#             [html.Tr([html.Th(col) for col in df.columns])]
#             + [
#                 html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
#                 for i in range(len(df))
#             ]
#         )
#
#     return df_to_table(df)
def get_safety_stock_table(warehouse, period, start_date, end_date):
    df = data.calculate_safety_stock((start_date, end_date))
    total_predict, _ = data.forecast(warehouse, period)
    total_predict = np.sum(total_predict)

    warehouse = f'Kho {warehouse}'
    df = df.loc[df['Kho'] == warehouse, :].drop(['Kho', 'period'], axis=1)
    df['Predict'] = np.ceil(total_predict * df['percentage'] / 100)
    df = clean_safety_stock_df(df)
    # print(df.columns)

    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        fixed_rows={'headers': True, 'data': 0},
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_cell={
            'whiteSpace': 'no-wrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            # 'width': 'auto',
            'maxHeight': "200px",
            'overflowY': 'scroll',
            'textAlign': 'left',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'right',
            } for c in df.columns[2:]
        ],
        # page_current=0,
        # page_size=20,
        # page_action='custom',

        # sort_action='custom',
        # sort_mode='single',
        # sort_by=[],

        style_as_list_view=True,
    ),
    return table


if __name__ == "__main__":
    app.run_server(debug=True)
