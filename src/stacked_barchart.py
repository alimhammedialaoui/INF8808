'''
    Contains some functions related to the creation of the stacked bar chart

'''

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()

    fig.update_layout(
        template=pio.templates['simple_white'],
        dragmode=False,
        barmode='relative',
    )

    return fig

def draw_stacked_barchart(fig, data):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    data["Valeurs"] = data["Valeurs"]*100
    fig = px.bar(data,
                 x ="Year",
                 y = "Valeurs",
                 range_y=[0, 100],
                 color="Taille",
                 labels={
                        "Valeurs": "% de Respect de l'obligation",
                        "Year": "Année",
                    },
                )
    return fig