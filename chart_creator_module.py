import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
import copy


class ChartCreator:
    """
    A class that will create the different figures that will be displayed on the dashboard.

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
    __create_specialized_df
        Generate a dataframe containing information (overall, mean, standard deviation and standard error) about a
        specific column in df (e.g., Genres, Distributors) with regards to different variables (e.g., Revenue, Rating).
    --extract_sms
        Generate a list containing information (overall, mean and standard deviation) about a specific column in df
        (e.g., Genres, Distributors) with regards to different variables (e.g., Revenue, Rating).
    __produce_color_lists
        Create a couple of lists comprised of the colors for the bars of a bar chart. One of the lists will be
        monochromatic and the other will have a different color for the bars representing the preferred user genres.
    __create_bar_chart
        Produce a bar chart figure for a specific set of data.
    __create_graph1_figs_mean_revenue
        Generate __fig1, __fig2, __fig3 and __fig4.
    __create_graph1_figs_overall_revenue
        Produce __fig5 and __fig6.
    __create_graph2_figs
        Create __fig7, __fig8 and __fig9.
    __create_graph3_fig
        Generate __fig10.
    __create_horizontal_barchart
        Produce a horizontal bar chart for the Distributor vs Mean Revenue relationship.
    __create_graph4_figs
        Create __fig11, __fig12 and __fig13.
    fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13
        Getter methods to obtain the private figures.

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
        self.__fig11, self.__fig12, self.__fig13 = self.__create_graph4_figs()

    def __create_df(self):
        """
        Create a dataframe containing the information from prepared_dataset.xlsx.

        Returns
        -------
        pandas.core.frame.DataFrame
            The generated dataframe.

        """
        df = pd.read_excel(self.__df_file, engine='openpyxl')
        df.drop(['Unnamed: 0'], axis=1, inplace=True)  # Drop the unnamed column that is generated when reading the file
        df['Genres'] = df['Genres'].apply(eval)  # Convert the genres column to list (it is in string format initially)
        return df

    def __create_specialized_df(self, column, column_elements, list_of_variables):
        """
        Produce a dataframe containing information (overall, mean, standard deviation and standard error) about a
        specific column in df (e.g., Genres, Distributors) with regards to different variables (e.g., Revenue, Rating).

        Arguments
        ---------
        column : str
            The name of the categorical column whose information we want extracted.
        column_elements : list
            The individual categorical elements that appear in column.
        list_of_variables : list
            The names of the numerical columns we want the information (overall, mean, standard deviation and standard
            error) to be calculated about (e.g., Revenue, Rating).

        Returns
        -------
        pandas.core.frame.DataFrame
            The dataframe that was created.

        """
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
        """
        Extract information (overall, mean and standard deviation) about specific column in df (e.g., Genres,
        Distributors) with regards to different variables (e.g., Revenue, Rating). This method will be used inside
        __create_specialized_df to extract the information that will be later introduced into a dataframe.

        Arguments
        ---------
        column : str
            The name of the categorical column whose information we want extracted.
        column_elements : list
            The individual categorical elements that appear in column.
        list_of_variables : list
            The names of the numerical columns we want the information (overall, mean, standard deviation and standard
            error) to be calculated about (e.g., Revenue, Rating).

        Returns
        -------
        list
            A list containing the extracted information.

        """
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

    def __produce_color_lists(self, base_color, secondary_color):
        """
        Create a couple of lists comprised of the colors for the bars of a bar chart. One of the lists will be
        monochromatic and the other will have a different color for the bars representing the preferred user genres.

        Arguments
        ---------
        base_color : str
            A string representing the base color for the bars.
        secondary_color : str
            A string representing the color that will be used for the preferred genre bars.

        Returns
        -------
        monochromatic_list : list
            A list containing the base color for each of the bars.
        pg_highlighted : list
            A list containing the secondary colors for the preferred genres and the base colors for the rest.

        """
        monochromatic_list = [base_color] * len(self.__genres_df.index)
        pg_highlighted = copy.copy(monochromatic_list)
        preferred_genres_pos = []
        genres_list = self.__genres_df['Genres'].tolist()
        for i in range(len(genres_list)):
            if genres_list[i] in self.__preferred_genres:
                preferred_genres_pos.append(i)

        for genre_pos, color in zip(preferred_genres_pos, pg_highlighted):
            pg_highlighted[genre_pos] = secondary_color

        return monochromatic_list, pg_highlighted

    @staticmethod
    def __create_bar_chart(data_x, data_y, bar_colors, customdata, hovertemplate, error=None):
        """
        Produce a bar chart figure for a specific set of data.

        Arguments
        ---------
        data_x : pandas.core.series.Series
            Pandas column that contains the x data.
        data_y : pandas.core.series.Series
            Pandas column that contains the y data.
        bar_colors : list
            A list containing the colors for the bars.
        customdata : numpy.ndarray
            An array containing the data that will be displayed when hovering over each bar.
        hovertemplate : str
            A string containing the format in which the information will be displayed when hovering over a bar.
        error : pandas.core.series.Series
            The pandas column that has the standard error that will be included in the chart. Default is none, which
            means no error bars will be shown.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            The bar chart created with the arguments provided.

        """
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
        """
        Create the four different figures that showcase the Mean Revenue vs Genre relationship.

        Returns
        -------
        fig1 : plotly.graph_objs._figure.Figure
            Mean Revenue vs Genre bar plot (monochromatic and no error bars).
        fig2 : plotly.graph_objs._figure.Figure
            Mean Revenue vs Genre bar plot (preferred genres highlighted and error bars).
        fig3 : plotly.graph_objs._figure.Figure
            Mean Revenue vs Genre bar plot (preferred genres highlighted and no error bars).
        fig4 : plotly.graph_objs._figure.Figure
            Mean Revenue vs Genre bar plot (monochromatic and error bars).

        """
        self.__genres_df.sort_values(by=['Mean Revenue'], inplace=True)
        monochromatic_list, pg_highlighted = self.__produce_color_lists('lightslategray', 'crimson')

        # Introduce custom_df and hovertemplate (they will be used to define the hover value of the figures)
        custom_df = np.stack((self.__genres_df['Mean Revenue'], self.__genres_df['Number of Movies']), axis=-1)
        hovertemplate = 'Mean Revenue: %{customdata[0]:.0f} (USD) <br><b>Number of Movies: %{customdata[1]:.0f}'

        # Create the four different figures
        fig1 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                       monochromatic_list, custom_df, hovertemplate)
        fig2 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                       pg_highlighted, custom_df, hovertemplate,
                                       self.__genres_df['Standard Error (Revenue)'])
        fig3 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                       pg_highlighted, custom_df, hovertemplate)
        fig4 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Mean Revenue'],
                                       monochromatic_list, custom_df, hovertemplate,
                                       self.__genres_df['Standard Error (Revenue)'])

        return fig1, fig2, fig3, fig4

    def __create_graph1_figs_overall_revenue(self):
        """
        Create the two figures that describe the Overall Revenue vs Genre relationship.

        Returns
        -------
        fig5 : plotly.graph_objs._figure.Figure
            Overall Revenue vs Genre bar plot (monochromatic).
        fig6 : plotly.graph_objs._figure.Figure
            Overall Revenue vs Genre bar plot (preferred genres highlighted).

        """
        self.__genres_df.sort_values(by=['Revenue'], inplace=True)
        monochromatic_list, pg_highlighted = self.__produce_color_lists('lightslategray', 'crimson')

        # Introduce custom_df and hovertemplate (they will be used to define the hover value of the figures)
        custom_df = np.stack((self.__genres_df['Revenue'], self.__genres_df['Number of Movies']), axis=-1)
        hovertemplate = 'Overall Revenue: %{customdata[0]:.0f} (USD) <br><b>Number of Movies: %{customdata[1]:.0f}'

        # Create both figures
        fig5 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Revenue'],
                                       monochromatic_list, custom_df, hovertemplate)
        fig6 = self.__create_bar_chart(self.__genres_df['Genres'], self.__genres_df['Revenue'],
                                       pg_highlighted, custom_df, hovertemplate)

        return fig5, fig6

    def __create_graph2_figs(self):
        """
        Create the four figures that display the information about runtime.

        Returns
        -------
        fig7 : plotly.graph_objs._figure.Figure
            Overall Revenue vs Runtime histogram.
        fig8 : plotly.graph_objs._figure.Figure
            Average Revenue vs Runtime histogram.
        fig9 : plotly.graph_objs._figure.Figure
            Count vs Runtime Histogram.

        """
        fig7 = px.histogram(self.__df, x='Runtime', y='Revenue', log_y=True, nbins=10)
        fig8 = px.histogram(self.__df, x='Runtime', y='Revenue', histfunc='avg', log_y=True, nbins=10)
        fig9 = px.histogram(self.__df, x='Runtime', nbins=10)
        return fig7, fig8, fig9

    def __create_graph3_fig(self):
        """
        Produce the Revenue vs Date Area plot figure.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            The generated figure.

        """
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
        fig10 = go.Figure(layout=layout)
        fig10.add_trace(
            go.Scatter(x=x_data, y=y_data, fill='tonexty'))  # Add the movie data

        # Add a green region (pre-covid area)
        fig10.add_vrect(
            x0="2018-01-01", x1="2020-03-15",
            fillcolor="rgb(0,255,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Pre-Lockdown', annotation_position='top left', annotation_font_color='grey'
        )

        # Add a red region (1st Lockdown area)
        fig10.add_vrect(
            x0="2020-03-15", x1="2020-07-15",
            fillcolor="rgb(255,0,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Lockdown', annotation_position='top left', annotation_font_color='grey'
        ),

        # Add a yellow region (post-lockdown)
        fig10.add_vrect(
            x0="2020-07-15", x1="2021-10-21",
            fillcolor="rgb(255,153,0)", opacity=0.3,
            layer="below", line_width=0,
            annotation_text='Post-Lockdown', annotation_position='top right', annotation_font_color='grey'
        )

        fig10.update_yaxes(range=[0, 2.9 * math.pow(10, 9)])
        fig10.update_layout(hovermode='x unified')
        return fig10

    def __create_horizontal_barchart(self, error=None):
        """
        Generate a horizontal bar plot to explain the Distributor vs Mean Revenue relationship.

        Arguments
        ---------
        error : pandas.core.series.Series
            The dataframe column that contains the standard error information. It is none by default, which means the
            error bars are not included.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            The created figure.

        """
        fig = go.Figure(layout=go.Layout(bargap=0.3))
        fig.add_trace(go.Bar(
            y=self.__dist_df['Distributor'], x=self.__dist_df['Mean Revenue'],
            error_x=dict(type='data', array=error),
            orientation='h'))
        fig.update_xaxes(type='log')
        fig.update_yaxes(tickfont_size=9)  # Any size above this one does not allow the labels to be seen
        return fig

    def __create_graph4_figs(self):
        """
        Produce the three figures that describe the relationship between Distributor and Revenue.

        Returns
        -------
        fig11 :  plotly.graph_objs._figure.Figure
            A treemap containing the Overall Revenue for each of the different Distributors.
        fig12 : plotly.graph_objs._figure.Figure
            A horizontal bar chart that showcases Distributor vs Mean Revenue (error bars included).
        fig13 : plotly.graph_objs._figure.Figure
            A horizontal bar chart that showcases Distributor vs Mean Revenue (no error bars).

        """
        fig11 = px.treemap(self.__dist_df, path=[px.Constant("Distribution Companies"), 'Distributor'],
                           values='Revenue',
                           color='Number of Movies',
                           color_continuous_scale='RdBu',
                           color_continuous_midpoint=np.average(self.__dist_df['Number of Movies'],
                                                                weights=self.__dist_df['Revenue']))

        self.__dist_df.sort_values(by=['Mean Revenue'], inplace=True)
        fig12 = self.__create_horizontal_barchart(self.__dist_df['Standard Error (Revenue)'])
        fig13 = self.__create_horizontal_barchart()
        return fig11, fig12, fig13

    @property
    def fig1(self):
        """Getter method to obtain fig1"""
        return self.__fig1

    @property
    def fig2(self):
        """Getter method to obtain fig2"""
        return self.__fig2

    @property
    def fig3(self):
        """Getter method to obtain fig3"""
        return self.__fig3

    @property
    def fig4(self):
        """Getter method to obtain fig4"""
        return self.__fig4

    @property
    def fig5(self):
        """Getter method to obtain fig5"""
        return self.__fig5

    @property
    def fig6(self):
        """Getter method to obtain fig6"""
        return self.__fig6

    @property
    def fig7(self):
        """Getter method to obtain fig7"""
        return self.__fig7

    @property
    def fig8(self):
        """Getter method to obtain fig8"""
        return self.__fig8

    @property
    def fig9(self):
        """Getter method to obtain fig9"""
        return self.__fig9

    @property
    def fig10(self):
        """Getter method to obtain fig10"""
        return self.__fig10

    @property
    def fig11(self):
        """Getter method to obtain fig11"""
        return self.__fig11

    @property
    def fig12(self):
        """Getter method to obtain fig12"""
        return self.__fig12

    @property
    def fig13(self):
        """Getter method to obtain fig13"""
        return self.__fig13
