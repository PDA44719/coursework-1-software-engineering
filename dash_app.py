# TODO: Add more interaction to the graphs (especially, the last ones).
#       Fix the height of the rows.
#       Include titles, modify axis labels, potentially change the styling (if required).
#       Include better names for the figures

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from chart_creator_module import ChartCreator
import collections

# Select the style sheet and define the app
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
cc = ChartCreator('prepared_dataset.xlsx')


# Create a function that contains the cards containing the images
def create_card(image_source, button_url):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Div([
                        html.H5('Revenue (per Movie) of Each Genre', className="card-title"),
                        dbc.CardImg(src=image_source),
                        html.P(
                            "Some quick example text to build on the card title and "
                            "make up the bulk of the card's content.",
                            className="card-text",
                        ),
                        dbc.Button("See Graph", color="primary", href=button_url),
                    ])
                ]
            ),
        ],
    )
    return card


main_page_layout = html.Div([
    html.H1(children='Dashboard'),
    html.Div(id='main_page_content'),
    dbc.Row([
        dbc.Col([create_card('assets/graph1.png', 'graph-page-1')], width=3),
        dbc.Col([create_card('assets/graph2.png', 'graph-page-2')], width=3),
        dbc.Col([create_card('assets/graph3.png', 'graph-page-3')], width=3),
        dbc.Col([create_card('assets/graph4.png', 'graph-page-4')], width=3),
        dbc.Col([create_card('assets/graph5.png', 'graph-page-5')], width=3)
    ]),
])


def create_checklist_card(checklist_id, checklist_options=[]):
    card = dbc.Card(className="bg-dark text-light", children=[
        dbc.CardBody([
            html.H4('Options', className="card-title"),
            html.Br(),
            dcc.Checklist(id=checklist_id, options=checklist_options)
        ])
    ])

    return card


def create_graph_page_with_dropdown(graph_id, dropdown_id, dropdown_options, starting_value, checklist_id):
    graph_page_layout = html.Div([
        html.H1(children='Specific Graph'),
        html.Div(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id=dropdown_id,
                    options=dropdown_options,
                    value=starting_value,
                    className='dropdown_list',
                    clearable=False  # Do not allow the dropdown value to be None
                ),
            ], width={"size": 6, "offset": 3})
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                create_checklist_card(checklist_id)
            ], width={"size": 2, "offset": 1}),
            dbc.Col([dcc.Graph(id=graph_id)], width=8)
        ]),
        dbc.Row([
            dbc.Col([dbc.Button("Go back to main page", color='primary', href='main-page')],
                    width={"size": 4, "offset": 8})
        ])
    ])

    return graph_page_layout


def layout_page_dropdown(graph_id, dropdown_id, dropdown_options, starting_value):
    graph_page_layout = html.Div([
        html.H1(children='Specific Graph'),
        html.Div(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id=dropdown_id,
                    options=dropdown_options,
                    value=starting_value,
                    className='dropdown_list',
                    clearable=False  # Do not allow the dropdown value to be None
                ),
            ], width={"size": 6, "offset": 3})
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id=graph_id)], width={"size": 8, "offset": 2})
        ]),
        dbc.Row([
            dbc.Col([dbc.Button("Go back to main page", color='primary', href='main-page')],
                    width={"size": 4, "offset": 8})
        ])
    ])

    return graph_page_layout


def create_simple_graph_page(fig):
    layout = html.Div([
        html.H1(children='Specific Graph'),
        html.Div(),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=fig)], width={"size": 8, "offset": 2})
        ]),
        dbc.Row([
            dbc.Col([dbc.Button("Go back to main page", color='primary', href='main-page')],
                    width={"size": 4, "offset": 8})
        ])
    ])

    return layout


def multiple_layout_with_dropdown(dropdown_id, dropdown_options, starting_value, row_id):
    graph_page_layout = html.Div([
        html.H1(children='Specific Graph'),
        html.Div(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id=dropdown_id,
                    options=dropdown_options,
                    value=starting_value,
                    className='dropdown_list',
                    clearable=False  # Do not allow the dropdown value to be None
                ),
            ], width={"size": 6, "offset": 3})
        ]),
        dbc.Row(id=row_id),  # This is the row that will be modified depending on the value of the dropdown
        dbc.Row([
            dbc.Col([dbc.Button("Go back to main page", color='primary', href='main-page')],
                    width={"size": 4, "offset": 8})
        ])
    ])

    return graph_page_layout


# Go through the different pages
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname')
              )
def navigate_pages(pathname):
    if pathname == '/graph-page-1':
        dropdown_options = [{'label': 'Genre Revenue per Movie', 'value': 'type1_1'},
                            {'label': 'Overall Genre Revenue', 'value': 'type1_2'}]
        return create_graph_page_with_dropdown('graph_1', 'dropdown1', dropdown_options, 'type1_1', 'chck1')

    if pathname == '/graph-page-2':
        dropdown_options = [{'label': 'Sum of Revenue', 'value': 'type2_1'},
                            {'label': 'Average of Revenue', 'value': 'type2_2'},
                            {'label': 'Number of movies', 'value': 'type2_3'}]
        return layout_page_dropdown('graph_2', 'dropdown2', dropdown_options, 'type2_1')

    if pathname == '/graph-page-3':
        return create_simple_graph_page(cc.fig6)

    if pathname == '/graph-page-4':
        dropdown_options = [{'label': 'Overall Distributor Revenue', 'value': 'type4_1'},
                            {'label': 'Average Distributor Revenue', 'value': 'type4_2'}]
        return multiple_layout_with_dropdown('dropdown4', dropdown_options, 'type4_1', 'modifiable_row')

    if pathname == '/graph-page-5':
        return create_simple_graph_page(cc.fig8)

    else:
        return main_page_layout


# Select the y axis for graph 1
@app.callback(Output('graph_1', component_property='figure'),
              Input('dropdown1', 'value'),
              Input('chck1', 'value'))
def change_y_axis(selected_y, selected_chart_options):
    # If selected_chart_options is None, convert to an empty list to avoid exception 'NoneType' is not iterable
    if selected_chart_options is None:
        selected_chart_options = []

    # If the user has not selected Show Preferred Genres option
    if selected_y == 'type1_2' and 'SPG' not in selected_chart_options:
        return cc.fig2
    elif selected_y == 'type1_2':  # If user has selected the Show Preferred Genres
        return cc.fig12
    elif selected_y == 'type1_1' and selected_chart_options == ['SPG']:
        return cc.fig10
    elif selected_y == 'type1_1' and selected_chart_options == ['SEB']:
        return cc.fig11
    elif selected_y == 'type1_1' and collections.Counter(selected_chart_options) == collections.Counter(['SEB', 'SPG']):
        return cc.fig9
    else:
        return cc.fig1


# Select the y axis for graph 1
@app.callback(Output('graph_2', component_property='figure'),
              [Input('dropdown2', 'value')])
def change_y_axis(value):
    if value == 'type2_1':
        return cc.fig3
    elif value == 'type2_2':
        return cc.fig4
    else:
        return cc.fig5


@app.callback(Output('chck1', 'options'),
              Input('dropdown1', 'value'))
def modify_checklist(dropdown_value):
    if dropdown_value == 'type1_1':
        return [{'label': 'Show Preferred Genres', 'value': 'SPG'},
                {'label': 'Show Error Bars', 'value': 'SEB'}]
    else:
        return [{'label': 'Show Preferred Genres', 'value': 'SPG'}]


@app.callback(Output('graph_4', 'figure'),
              Input('dropdown4', 'value'))
def update_graph4_layout(dropdown_value):
    if dropdown_value == 'type4_2':
        return cc.fig8
    else:
        return cc.fig7


@app.callback(Output('modifiable_row', 'children'),
              Input('dropdown4', 'value'))
def modify_graph4_row(dropdown_value):
    if dropdown_value == 'type4_1':
        return dbc.Col([dcc.Graph(id='graph_4')], width={"size": 8, "offset": 2})
    else:
        row_layout = dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                create_checklist_card('chck4')
            ], width={"size": 2, "offset": 1}),
            dbc.Col([dcc.Graph(id='graph_4')], width=8)
        ])
        return row_layout


@app.callback(Output('chck4', 'options'),
              Input('dropdown4', 'value'))
def define_chck4_options(dropdown_value):
    if dropdown_value == 'type4_2':
        options = [{'label': 'Show Error Bars', 'value': 'SEB'}]
        return options
    else:
        return []


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
