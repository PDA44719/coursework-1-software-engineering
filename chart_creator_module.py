import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
import copy


class ChartCreator:
    def __init__(self, dataset_file):
        self.__df_file = dataset_file
        self.__df = self.__create_df()
        self.__genres_df = self.__create_genres_df()
        self.__dist_df = self.__create_distributors_df()
        self.__fig1, self.__fig2, self.__fig9, self.__fig10, self.__fig11, self.__fig12 = self.__create_figs_12910()
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
        genres_no_repetition = list(set([genre for column_data in self.__df['Genres'] for genre in column_data]))
        genres_info = self.__extract_sms('Genres', genres_no_repetition, ['Revenue', 'Rating'])
        genres_df = pd.DataFrame(genres_info,
                                 columns=['Genre', 'Revenue', 'Mean Revenue', 'SD Revenue', 'Rating', 'Mean Rating',
                                          'SD Rating', 'Number of Movies']
                                 )
        genres_df['Standard Error (Revenue)'] = genres_df.apply(
            lambda x: round(x['SD Revenue'] / math.sqrt(x['Number of Movies']), 2), axis=1)
        return genres_df

    def __create_distributors_df(self):
        # Get a list of the different distribution companies
        list_of_distributors_with_repetition = [element for element in self.__df['Distributor']]
        list_of_distributors_no_repetition = list(set(list_of_distributors_with_repetition))

        # Extract information about each of the distribution companies
        info = self.__extract_sms('Distributor', list_of_distributors_no_repetition, ['Revenue', 'Rating'])
        dist_df = pd.DataFrame(info,
                               columns=['Distributor', 'Revenue', 'Mean Revenue', 'SD Revenue', 'Rating', 'Mean Rating',
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

    def __produce_color_list(self, preferred_genres, base_color, secondary_color):
        color_list = [base_color] * len(self.__genres_df.index)
        preferred_genres_pos = []
        genres_list = self.__genres_df['Genre'].tolist()
        for i in range(len(genres_list)):
            if genres_list[i] in preferred_genres:
                preferred_genres_pos.append(i)

        for genre_pos, color in zip(preferred_genres_pos, color_list):
            color_list[genre_pos] = secondary_color

        return color_list

    @staticmethod
    def __create_bar_chart(data_x, data_y, bar_colors, customdata, hovertemplate, error=None):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_x,
            y=data_y,
            customdata=customdata,
            marker_color=bar_colors,  # marker color can be a single color value or an iterable
            hovertemplate=hovertemplate,
            error_y=dict(type='data', array=error),
            name=''
        ))
        fig.update_layout(template='plotly_white')

        return fig

    def __create_figs_12910(self):
        preferred_genres = ['History', 'Romance', 'Action']
        # Sort values for the first plot
        self.__genres_df.sort_values(by=['Mean Revenue'], inplace=True)
        colors_fig1 = ['lightslategray'] * len(self.__genres_df.index)
        custom_df19 = np.stack((self.__genres_df['Mean Revenue'], self.__genres_df['Number of Movies']), axis=-1)
        hovertemplate_fig19 = 'Mean Revenue: %{customdata[0]:.0f} (USD) <br><b>Number of Movies: %{customdata[1]:.0f}'
        colors_fig9 = self.__produce_color_list(preferred_genres, 'lightslategray', 'crimson')

        fig1 = self.__create_bar_chart(self.__genres_df['Genre'], self.__genres_df['Mean Revenue'],
                                       colors_fig1, custom_df19, hovertemplate_fig19)

        fig9 = self.__create_bar_chart(self.__genres_df['Genre'], self.__genres_df['Mean Revenue'],
                                       colors_fig9, custom_df19, hovertemplate_fig19,
                                       self.__genres_df['Standard Error (Revenue)'])

        fig10 = self.__create_bar_chart(self.__genres_df['Genre'], self.__genres_df['Mean Revenue'],
                                        colors_fig9, custom_df19, hovertemplate_fig19)

        fig11 = self.__create_bar_chart(self.__genres_df['Genre'], self.__genres_df['Mean Revenue'],
                                        colors_fig1, custom_df19, hovertemplate_fig19,
                                        self.__genres_df['Standard Error (Revenue)'])

        # Resort the values and generate fig2
        self.__genres_df.sort_values(by=['Revenue'], inplace=True)

        colors_fig2 = self.__produce_color_list(preferred_genres, 'lightslategray', 'crimson')
        custom_df2 = np.stack((self.__genres_df['Revenue'], self.__genres_df['Number of Movies']), axis=-1)
        hovertemplate_fig2 = 'Overall Revenue: %{customdata[0]:.0f} (USD) <br><b>Number of Movies: %{customdata[1]:.0f}'
        fig2 = self.__create_bar_chart(self.__genres_df['Genre'], self.__genres_df['Revenue'],
                                       colors_fig1, custom_df2, hovertemplate_fig2)
        fig12 = self.__create_bar_chart(self.__genres_df['Genre'], self.__genres_df['Revenue'],
                                        colors_fig2, custom_df2, hovertemplate_fig2)

        return fig1, fig2, fig9, fig10, fig11, fig12

    def __create_figs_345(self):
        fig3 = px.histogram(self.__df, x='Runtime', y='Revenue', log_y=True, nbins=10)
        fig4 = px.histogram(self.__df, x='Runtime', y='Revenue', histfunc='avg', log_y=True, nbins=10)
        fig5 = px.histogram(self.__df, x='Runtime', nbins=10)
        return fig3, fig4, fig5

    def __create_f6(self):
        # Get the x data value
        x_data = []
        for index, row in self.__df.iterrows():
            if row['Release Date'] not in x_data:
                x_data.append(row['Release Date'])

        # Get the y data
        y_data = []
        for date in x_data:
            y_data.append(sum([row['Revenue'] for index, row in self.__df.iterrows() if date == row['Release Date']]))

        layout = go.Layout(template='plotly_white')
        fig6 = go.Figure(layout=layout)
        fig6.add_trace(
            go.Scatter(x=x_data, y=y_data, fill='tonexty'))  # Add the movie data

        # Add a green region (pre-covid area)
        fig6.add_vrect(
            x0="2018-01-01", x1="2020-03-15",
            fillcolor="rgb(0,255,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Pre-Lockdown', annotation_position='top left', annotation_font_color='grey'
        )

        # Add a red region (1st Lockdown area)
        fig6.add_vrect(
            x0="2020-03-15", x1="2020-07-15",
            fillcolor="rgb(255,0,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Lockdown', annotation_position='top left', annotation_font_color='grey'
        ),

        # Add a yellow region (post-lockdown)
        fig6.add_vrect(
            x0="2020-07-15", x1="2021-10-21",
            fillcolor="rgb(255,153,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Post-Lockdown', annotation_position='top right', annotation_font_color='grey'
        )

        fig6.update_yaxes(range=[0, 2.9 * math.pow(10, 9)])
        fig6.update_layout(hovermode='x unified')
        return fig6

    def __create_figs_78(self):
        fig7 = px.treemap(self.__dist_df, path=[px.Constant("Distribution Companies"), 'Distributor'], values='Revenue',
                          color='Number of Movies',
                          color_continuous_scale='RdBu',
                          color_continuous_midpoint=np.average(self.__dist_df['Number of Movies'],
                                                               weights=self.__dist_df['Revenue']))

        self.__dist_df['Standard Error (Revenue)'] = self.__dist_df.apply(
            lambda x: round(x['SD Revenue'] / math.sqrt(x['Number of Movies']), 2), axis=1)
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

    @property
    def fig9(self):
        return self.__fig9

    @property
    def fig10(self):
        return self.__fig10

    @property
    def fig11(self):
        return self.__fig11

    @property
    def fig12(self):
        return self.__fig12
