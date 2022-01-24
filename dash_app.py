# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Output, Input

# Select the style sheet and define the app
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

# Read the Excel file and generate the dataset
df = pd.read_excel('prepared_dataset.xlsx', engine='openpyxl')  # Read the dataset
df.drop(['Unnamed: 0'], axis=1, inplace=True)  # Drop the unnamed column

# Extract all the genres in the dataframe
df['Genres'] = df['Genres'].apply(eval)  # Convert the genres column to list (it is in string format initially)
list_of_genres = [genre for column_data in df['Genres'] for genre in column_data]

# Obtain the set of genres (no repetition)
set_of_genres = set()
for genre in list_of_genres:
    set_of_genres.add(genre)

# Get the number of movies that contain each genre, the total revenue and the average rating
genres = list(set_of_genres)  # Convert the genres back to a list
n_of_movies = []
genre_revenue = []
total_rating = []
for i in range(len(genres)):
    # Each of the categories will start at 0
    n_of_movies.append(0)
    genre_revenue.append(0)
    total_rating.append(0)

    # Go through each of the movies and update the three categories
    for index, row in df.iterrows():  # Iterate through the dataframe rows
        if genres[i] in row['Genres']:  # If the movie contains the specific genre in the list
            # Update categories
            n_of_movies[i] = n_of_movies[i] + 1
            genre_revenue[i] = genre_revenue[i] + row['Revenue']
            total_rating[i] = total_rating[i] + row['Rating']

    # Get the average revenue per movie for each of the genres
    revenue_per_movie = []
    for i in range(len(genre_revenue)):
        revenue_per_movie.append(round((genre_revenue[i] / n_of_movies[i]), 2))

    # Get the average rating of each genre
    average_rating = []
    for i in range(len(total_rating)):
        average_rating.append(round((total_rating[i] / n_of_movies[i]), 2))

    # Create the new dataframe
    genres_df = pd.DataFrame(list(zip(genres, n_of_movies, genre_revenue, revenue_per_movie, average_rating)),
                             columns=['Genre', 'Number of Movies', 'Overall Genre Revenue', 'Genre Revenue per Movie',
                                      'Average Rating'])

    # Sort values for the first plot
    genres_df.sort_values(by=['Genre Revenue per Movie'], inplace=True)

    fig1 = px.bar(genres_df, x='Genre', y='Genre Revenue per Movie',
                  hover_data=['Overall Genre Revenue', 'Number of Movies'],
                  labels={'Genre Revenue per Movie': 'Genre Revenue per Movie (USD)',
                          'Overall Genre Revenue': 'Overall Genre Revenue (USD)'})

    # Resort the values and generate fig2
    genres_df.sort_values(by=['Overall Genre Revenue'], inplace=True)
    fig2 = px.bar(genres_df, x='Genre', y='Overall Genre Revenue',
                  hover_data=['Genre Revenue per Movie', 'Number of Movies'],
                  labels={'Genre Revenue per Movie': 'Genre Revenue per Movie (USD)',
                          'Overall Genre Revenue': 'Overall Genre Revenue (USD)'},
                  )

# Create the card containing the first image
card1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div([
                    html.H5('Revenue (per Movie) of Each Genre', className="card-title"),
                    dbc.CardImg(src='assets/graph1.png'),
                    html.P(
                        "Some quick example text to build on the card title and "
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button("See Graph", color="primary", href='graph-page'),
                ])
            ]
        ),
    ],
)

main_page_layout = html.Div([
    html.H1(children='Dashboard'),
    html.Div(id='main_page_content'),
    dbc.Row([
        dbc.Col([card1], width=3), dbc.Col([card1], width=3), dbc.Col([card1], width=3), dbc.Col([card1], width=3),
        dbc.Col([card1], width=3), dbc.Col([card1], width=3)
    ]),
])

graph_page_layout = html.Div([
    html.H1(children='Specific Graph'),
    html.Div(id='graph_page_content'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='dropdown1',
                options=[
                    {'label': 'Genre Revenue per Movie', 'value': 'type1'},
                    {'label': 'Overall Genre Revenue', 'value': 'type2'}
                ],
                value='type1',  # Starting on the Genre Revenue per Move
                clearable=False  # Do not allow the dropdown value to be None
            ),
        ], width={"size": 6, "offset": 3})
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='graph_1')], width={"size": 6, "offset": 3})
    ]),
    dbc.Row([
        dbc.Col([dbc.Button("Go back to main page", color='primary', href='main-page')], width={"size": 4, "offset": 8})
    ])
])


# Go through the different pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def navigate_pages(pathname):
    if pathname == '/graph-page':
        return graph_page_layout
    else:
        return main_page_layout


# Select the y axis for graph 1
@app.callback(Output('graph_1', component_property='figure'),
              [Input('dropdown1', 'value')])
def change_y_axis(value):
    if value == 'type1':
        return fig1
    else:
        return fig2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
