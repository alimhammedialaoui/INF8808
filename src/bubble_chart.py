import plotly.express as px
import hover_template


def get_plot(my_df):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled, and there is
        an animation between the data for years 2000 and 2015.

        The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

        The markers' maximum size is 30 and their minimum
        size is 6.

        Args:
            my_df: The dataframe to display
            gdp_range: The range for the x axis
            co2_range: The range for the y axis
        Returns:
            The generated figure
    '''
    # TODO : Define figure with animation
    fig = px.scatter(my_df,
                     x='Declarer',
                     y='Produire',
                     size = "Ratio",
                     text=list(map(lambda n:round(n,2),list(my_df["Ratio"].values)))
                     )
    fig.update_traces(marker=dict(sizemin=7,color="orange",opacity=1),textposition="middle center")

    return fig