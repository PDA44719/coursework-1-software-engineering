# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from chart_creator_module import ChartCreator

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
        dbc.Col([create_card('assets/graph1.png', 'graph-page-1')], width=3),
        dbc.Col([create_card('assets/graph1.png', 'graph-page-1')], width=3),
        dbc.Col([create_card('assets/graph1.png', 'graph-page-1')], width=3),
        dbc.Col([create_card('assets/graph1.png', 'graph-page-1')], width=3)
    ]),
])


def create_graph_page_with_dropdown(graph_id, dropdown_id, dropdown_options, starting_value):
    graph_page_layout = html.Div([
        html.H1(children='Specific Graph'),
        html.Div(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id=dropdown_id,
                    options=dropdown_options,
                    value=starting_value,  # Starting on the Genre Revenue per Move
                    clearable=False  # Do not allow the dropdown value to be None
                ),
            ], width={"size": 6, "offset": 3})
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id=graph_id)], width={"size": 6, "offset": 3})
        ]),
        dbc.Row([
            dbc.Col([dbc.Button("Go back to main page", color='primary', href='main-page')],
                    width={"size": 4, "offset": 8})
        ])
    ])

    return graph_page_layout


# Go through the different pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def navigate_pages(pathname):
    if pathname == '/graph-page-1':
        dropdown_options = [{'label': 'Genre Revenue per Movie', 'value': 'type1_1'},
                            {'label': 'Overall Genre Revenue', 'value': 'type1_2'}]
        return create_graph_page_with_dropdown('graph_1', 'dropdown1', dropdown_options, 'type1_1')

    if pathname == '/graph-page-2':
        dropdown_options = [{'label': 'Sum of Revenue', 'value': 'type2_1'},
                            {'label': 'Average of Revenue', 'value': 'type2_2'},
                            {'label': 'Number of movies', 'value': 'type2_3'}]
        return create_graph_page_with_dropdown('graph_2', 'dropdown2', dropdown_options, 'type2_1')

    else:
        return main_page_layout


# Select the y axis for graph 1
@app.callback(Output('graph_1', component_property='figure'),
              [Input('dropdown1', 'value')])
def change_y_axis(value):
    if value == 'type1_1':
        return cc.fig1
    else:
        return cc.fig2


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


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
