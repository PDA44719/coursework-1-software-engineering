import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
import copy


class ChartCreator:
    """
    A class that will create the different charts that will be displayed on the dashboard.

    Arguments
    ---------
    dataset_path : str
        The path to the file containing the dataset (prepared_dataset.xlsx).

    Attributes
    ----------
    __df : pandas.core.frame.DataFrame
        The dataframe obtained by reading prepared_dataset.xlsx.
    __genres_df : pandas.core.frame.DataFrame
        A dataframe containing information about each individual genre that appears on df['Genres'].
    __dist_df : pandas.core.frame.DataFrame
        A dataframe containing information about each distribution company that appears on df['Distributor'].
    __preferred_genres : list
        A list containing the preferred genres of the user. In this case, the preferred genres defined in persona.png
        will be utilized.
    __fig1, __fig2, __fig3, __fig4 : plotly.graph_objs._figure.Figure
        Different options for the Mean Revenue vs Genre bar chart (i.e., graph 1).
    __fig5, __fig6 : plotly.graph_objs._figure.Figure
        Different options for the Overall Revenue vs Genre bar plot (i.e., graph 1).
    __fig7, __fig8, __fig9 : plotly.graph_objs._figure.Figure
        Different options for the Runtime histograms (i.e., graph 2).
    __fig10 : plotly.graph_objs._figure.Figure
        Revenue before, during and after lockdown Area plot (i.e., graph 3).
    __fig11 : plotly.graph_objs._figure.Figure
        Revenue by distribution company Treemap (i.e., graph 4).
    __fig12, __fig13 : plotly.graph_objs._figure.Figure
        Different options for the Distribution Company vs Mean Revenue bar plot (i.e., graph 4).

    Methods
    -------
    __create_df
        Read prepared_dataset.xlsx and convert to a dataframe.
    __create_genres_df
        Obtain information (overall, mean and standard deviation) about each movie genre in df.
    __create_distributors_df
        Obtain information
    *******
    """

    def __init__(self, dataset_path):
        self.__df_file = dataset_path
        self.__df = self.__create_df()
        self.__genres_list = list(set([genre for column_data in self.__df['Genres'] for genre in column_data]))
        self.__distributors_list = list(set([element for element in self.__df['Distributor']]))
        self.__genres_df = self.__create_specialized_df('Genres', self.__genres_list, ['Revenue'])
        self.__dist_df = self.__create_specialized_df('Distributor', self.__distributors_list, ['Revenue'])
        self.__preferred_genres = ['History', 'Romance', 'Action']
        self.__fig1, self.__fig2, self.__fig3, self.__fig4 = self.__create_graph1_figs_mean_revenue()
        self.__fig5, self.__fig6 = self.__create_graph1_figs_overall_revenue()
        self.__fig7, self.__fig8, self.__fig9 = self.__create_graph2_figs()
        self.__fig10 = self.__create_graph3_fig()
        self.__fig11, self.__fig12, self.__fig13 = self.__create_figs_78()

    def __create_df(self):
        # Read the Excel file and generate the dataset
        df = pd.read_excel(self.__df_file, engine='openpyxl')  # Read the dataset
        df.drop(['Unnamed: 0'], axis=1, inplace=True)  # Drop the unnamed column
        df['Genres'] = df['Genres'].apply(eval)  # Convert the genres column to list (it is in string format initially)
        return df

    def __create_specialized_df(self, column, column_elements, list_of_variables):
        info = self.__extract_sms(column, column_elements, list_of_variables)
        dataframe_columns = [column]
        for variable in list_of_variables:
            dataframe_columns.extend([variable, f'Mean {variable}', f'SD {variable}'])
        dataframe_columns.append('Number of Movies')
        specialized_df = pd.DataFrame(info, columns=dataframe_columns)

        # Create a new column containing the Standard Error (the formula is SE = SD / sqrt(n of samples))
        for variable in list_of_variables:
            specialized_df[f'Standard Error ({variable})'] = specialized_df.apply(
                lambda x: round(x[f'SD {variable}'] / math.sqrt(x['Number of Movies']), 2), axis=1)
        return specialized_df

    def __extract_sms(self, column, column_elements, list_of_variables):
        output_list = []
        for element in column_elements:  # Go through the different categories
            output_list.append([element])
            for variable in list_of_variables:
                values = []
                for index, row in self.__df.iterrows():
                    if element in row[column]:
                        values.append(row[variable])
                output_list[-1].append(sum(values))  # Append the Summation value
                output_list[-1].append(sum(values) / len(values))  # Append the Mean value
                output_list[-1].append(np.std(values))  # Append the Standard Deviation value
            output_list[-1].append(len(values))  # Number of movies
        return output_list

    def __produce_color_lists(self, preferred_genres, base_color, secondary_color):
        monochromatic_list = [base_color] * len(self.__genres_df.index)
        pg_highlighted = copy.copy(monochromatic_list)
        preferred_genres_pos = []
        genres_list = self.__genres_df['Genres'].tolist()
        for i in range(len(genres_list)):
            if genres_list[i] in preferred_genres:
                preferred_genres_pos.append(i)

        for genre_pos, color in zip(preferred_genres_pos, pg_highlighted):
            pg_highlighted[genre_pos] = secondary_color

        return monochromatic_list, pg_highlighted

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

    def __create_graph1_figs_mean_revenue(self):
        self.__genres_df.sort_values(by=['Mean Revenue'], inplace=True)
        monochromatic_list, pg_highlighted = self.__produce_color_lists(self.__preferred_genres, 'lightslategray',
                                                                        'crimson')

        # Introduce custom_df and hovertemplate (they will be used to define the hover value of the figures)
        custom_df = np.stack((self.__genres_df['Mean Revenue'], self.__genres_df['Number of Movies']), axis=-1)
        hovertemplate = 'Mean Revenue: %{customdata[0]:.0f} (USD) <br><b>Number of Movies: %{customdata[1]:.0f}'

        # Create a chart of the mean revenue for each genre (monochromatic and no error bars)
        fig1 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                       monochromatic_list, custom_df, hovertemplate)

        # Create a chart of the mean revenue for each genre (preferred genres highlighted and error bars)
        fig2_ = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                        pg_highlighted, custom_df, hovertemplate,
                                        self.__genres_df['Standard Error (Revenue)'])

        # Create a chart of the mean revenue for each genre (preferred genres highlighted and no error bars)
        fig3_ = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                        pg_highlighted, custom_df, hovertemplate)

        # Create a chart of the mean revenue for each genre (monochromatic and error bars)
        fig4_ = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                        monochromatic_list, custom_df, hovertemplate,
                                        self.__genres_df['Standard Error (Revenue)'])

        return fig1, fig2_, fig3_, fig4_

    def __create_graph1_figs_overall_revenue(self):
        self.__genres_df.sort_values(by=['Revenue'], inplace=True)
        monochromatic_list, pg_highlighted = self.__produce_color_lists(self.__preferred_genres, 'lightslategray',
                                                                        'crimson')

        # Introduce custom_df and hovertemplate (they will be used to define the hover value of the figures)
        custom_df = np.stack((self.__genres_df['Revenue'], self.__genres_df['Number of Movies']), axis=-1)
        hovertemplate = 'Overall Revenue: %{customdata[0]:.0f} (USD) <br><b>Number of Movies: %{customdata[1]:.0f}'

        # Create a chart of the overall revenue for each genre (monochromatic)
        fig5_ = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Revenue'],
                                        monochromatic_list, custom_df, hovertemplate)

        # Create a chart of the overall revenue for each genre (preferred genres highlighted)
        fig6_ = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Revenue'],
                                        pg_highlighted, custom_df, hovertemplate)

        return fig5_, fig6_

    def __create_graph2_figs(self):
        fig7_ = px.histogram(self.__df, x='Runtime', y='Revenue', log_y=True, nbins=10)
        fig8_ = px.histogram(self.__df, x='Runtime', y='Revenue', histfunc='avg', log_y=True, nbins=10)
        fig9_ = px.histogram(self.__df, x='Runtime', nbins=10)
        return fig7_, fig8_, fig9_

    def __create_graph3_fig(self):
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
        fig10_ = go.Figure(layout=layout)
        fig10_.add_trace(
            go.Scatter(x=x_data, y=y_data, fill='tonexty'))  # Add the movie data

        # Add a green region (pre-covid area)
        fig10_.add_vrect(
            x0="2018-01-01", x1="2020-03-15",
            fillcolor="rgb(0,255,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Pre-Lockdown', annotation_position='top left', annotation_font_color='grey'
        )

        # Add a red region (1st Lockdown area)
        fig10_.add_vrect(
            x0="2020-03-15", x1="2020-07-15",
            fillcolor="rgb(255,0,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Lockdown', annotation_position='top left', annotation_font_color='grey'
        ),

        # Add a yellow region (post-lockdown)
        fig10_.add_vrect(
            x0="2020-07-15", x1="2021-10-21",
            fillcolor="rgb(255,153,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Post-Lockdown', annotation_position='top right', annotation_font_color='grey'
        )

        fig10_.update_yaxes(range=[0, 2.9 * math.pow(10, 9)])
        fig10_.update_layout(hovermode='x unified')
        return fig10_

    def __create_horizontal_barchart(self, error=None):
        fig = go.Figure(layout=go.Layout(bargap=0.3))
        fig.add_trace(go.Bar(
            y=self.__dist_df['Distributor'], x=self.__dist_df['Mean Revenue'],
            error_x=dict(type='data', array=error),
            orientation='h'))
        fig.update_xaxes(type='log')
        fig.update_yaxes(tickfont_size=9)  # Any size above this one does not allow the labels to be seen
        return fig

    def __create_figs_78(self):
        fig11_ = px.treemap(self.__dist_df, path=[px.Constant("Distribution Companies"), 'Distributor'], values='Revenue',
                            color='Number of Movies',
                            color_continuous_scale='RdBu',
                            color_continuous_midpoint=np.average(self.__dist_df['Number of Movies'],
                                                                 weights=self.__dist_df['Revenue']))

        self.__dist_df['Standard Error (Revenue)'] = self.__dist_df.apply(
            lambda x: round(x['SD Revenue'] / math.sqrt(x['Number of Movies']), 2), axis=1)
        self.__dist_df.sort_values(by=['Mean Revenue'], inplace=True)
        fig12_ = self.__create_horizontal_barchart(self.__dist_df['Standard Error (Revenue)'])
        fig13 = self.__create_horizontal_barchart()
        return fig11_, fig12_, fig13

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

    @property
    def fig13(self):
        return self.__fig13
