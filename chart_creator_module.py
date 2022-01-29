import plotly.express as px
import pandas as pd


class ChartCreator:
    def __init__(self, dataset_file):
        self.__df_file = dataset_file
        self.__df = self.__create_df()
        self.__genres_df = self.__create_genres_df()
        self.__fig1, self.__fig2 = self.__create_figs_12()
        self.__fig3, self.__fig4, self.__fig5 = self.__create_figs_345()

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
