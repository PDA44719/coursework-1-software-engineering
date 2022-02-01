import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math


class ChartCreator:
    def __init__(self, dataset_file):
        self.__df_file = dataset_file
        self.__df = self.__create_df()
        self.__genres_df = self.__create_genres_df()
        self.__dist_df = self.__create_distributors_df()
        self.__fig1, self.__fig2 = self.__create_figs_12()
        self.__fig3, self.__fig4, self.__fig5 = self.__create_figs_345()
        self.__fig6 = self.__create_f6()
        self.__fig7, self.__fig8 = self.__create_figs_78()

    def __create_df(self):
        # Read the Excel file and generate the dataset
        df = pd.read_excel(self.__df_file, engine='openpyxl')  # Read the dataset
        df.drop(['Unnamed: 0'], axis=1, inplace=True)  # Drop the unnamed column
        df['Genres'] = df['Genres'].apply(eval)  # Convert the genres column to list (it is in string format initially)
        return df

    def __create_genres_df(self):
        list_of_genres = [genre for column_data in self.__df['Genres'] for genre in column_data]

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
            for index, row in self.__df.iterrows():  # Iterate through the dataframe rows
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
                                 columns=['Genre', 'Number of Movies', 'Overall Genre Revenue',
                                          'Genre Revenue per Movie',
                                          'Average Rating'])
        return genres_df

    def __create_distributors_df(self):
        # Get a list of the different distribution companies
        list_of_distributors_with_repetition = [element for element in self.__df['Distributor']]
        list_of_distributors_no_repetition = list(set(list_of_distributors_with_repetition))

        # Extract information about each of the distribution companies
        info = self.__extract_sms('Distributor', list_of_distributors_no_repetition, ['Revenue', 'Rating'])
        dist_df = pd.DataFrame(info, columns=['Distributor', 'Revenue', 'Mean Revenue', 'SD Revenue', 'Rating', 'Mean Rating',
                                              'SD Rating', 'Number of Movies'])
        return dist_df

    def __extract_sms(self, column, column_elements, list_of_variables):
        output_list = []
        for element in column_elements:  # Go through the different categories
            output_list.append([element])
            for variable in list_of_variables:
                values = []
                for index, row in self.__df.iterrows():
                    if element in row[column]:
                        values.append(row[variable])
                # Append the summation, mean and standard deviation of the values
                output_list[-1].append(sum(values))  # Summation
                output_list[-1].append(sum(values) / len(values))  # Mean
                output_list[-1].append(round(np.std(values), 2))  # SD
            output_list[-1].append(len(values))  # Number of movies
        return output_list

    def __create_figs_12(self):
        # Sort values for the first plot
        self.__genres_df.sort_values(by=['Genre Revenue per Movie'], inplace=True)

        fig1 = px.bar(self.__genres_df, x='Genre', y='Genre Revenue per Movie',
                      hover_data=['Overall Genre Revenue', 'Number of Movies'],
                      labels={'Genre Revenue per Movie': 'Genre Revenue per Movie (USD)',
                              'Overall Genre Revenue': 'Overall Genre Revenue (USD)'})

        # Resort the values and generate fig2
        self.__genres_df.sort_values(by=['Overall Genre Revenue'], inplace=True)
        fig2 = px.bar(self.__genres_df, x='Genre', y='Overall Genre Revenue',
                      hover_data=['Genre Revenue per Movie', 'Number of Movies'],
                      labels={'Genre Revenue per Movie': 'Genre Revenue per Movie (USD)',
                              'Overall Genre Revenue': 'Overall Genre Revenue (USD)'},
                      )
        return fig1, fig2

    def __create_figs_345(self):
        fig3 = px.histogram(self.__df, x='Runtime', y='Revenue', log_y=True, nbins=10)
        fig4 = px.histogram(self.__df, x='Runtime', y='Revenue', histfunc='avg', log_y=True, nbins=10)
        fig5 = px.histogram(self.__df, x='Runtime', nbins=10)
        return fig3, fig4, fig5

    def __create_f6(self):
        layout = go.Layout(template='simple_white')
        fig6 = go.Figure(layout=layout)
        fig6.add_trace(
            go.Scatter(x=self.__df['Release Date'], y=self.__df['Revenue'], fill='tonexty'))  # Add the movie data

        # Add a green region (pre-covid area)
        fig6.add_vrect(
            x0="2018-01-01", x1="2020-03-15",
            fillcolor="rgb(0,255,0)", opacity=0.3,
            layer="below", line_width=0,
        )

        # Add a red region (1st Lockdown area)
        fig6.add_vrect(
            x0="2020-03-15", x1="2020-07-15",
            fillcolor="rgb(255,0,0)", opacity=0.3,
            layer="below", line_width=0,
        ),

        # Add a yellow region (post-lockdown)
        fig6.add_vrect(
            x0="2020-07-15", x1="2021-10-21",
            fillcolor="rgb(255,153,0)", opacity=0.3,
            layer="below", line_width=0,
        )

        fig6.update_yaxes(range=[0, 2.9 * math.pow(10, 9)])
        fig6.update_layout(hovermode='x unified')
        return fig6

    def __create_figs_78(self):
        fig7 = px.treemap(self.__dist_df, path=[px.Constant("Distribution Companies"), 'Distributor'], values='Revenue',
                          color='Number of Movies',
                          color_continuous_scale='RdBu',
                          color_continuous_midpoint=np.average(self.__dist_df['Number of Movies'], weights=self.__dist_df['Revenue']))

        self.__dist_df['Standard Error (Revenue)'] = self.__dist_df.apply(lambda x: round(x['SD Revenue']/math.sqrt(x['Number of Movies']), 2), axis=1)
        self.__dist_df.sort_values(by=['Mean Revenue'], inplace=True)
        fig8 = go.Figure(layout=go.Layout(bargap=0.3))
        fig8.add_trace(go.Bar(
            y=self.__dist_df['Distributor'], x=self.__dist_df['Mean Revenue'],
            # width = [0.3]*30,
            error_x=dict(type='data', array=self.__dist_df['Standard Error (Revenue)']),
            orientation='h'))
        fig8.update_xaxes(type='log')
        fig8.update_yaxes(tickfont_size=9)  # Any size above this one does not allow the labels to be seen
        return fig7, fig8

    @property
    def fig1(self):
        return self.__fig1

    @property
    def fig2(self):
        return self.__fig2

    @property
    def fig3(self):
        return self.__fig3

    @property
    def fig4(self):
        return self.__fig4

    @property
    def fig5(self):
        return self.__fig5

    @property
    def fig6(self):
        return self.__fig6

    @property
    def fig7(self):
        return self.__fig7

    @property
    def fig8(self):
        return self.__fig8
