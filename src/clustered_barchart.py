'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import hover_template as hover

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


def draw_clustered_barchart(fig, data_anim):
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
    
    fig = px.bar(data_anim, 
                 x=data_anim['Lois'], 
                 y=data_anim['Valeurs']*100, 
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 barmode = 'group',
                 range_y=[0,100], 
                 color=data_anim['Obligation'],
                 labels={
                        "Valeurs": "Respect de l'obligation",
                        "Lois": "Lois fiscales",
                        "Obligation": "Obligations fiscales"
                    },
                 title='Analyse des lois selon les obligations applicables'
                )
    fig.update_layout(title_x = 0.5, yaxis_title="% de respect de l'obligation")
    fig.update_traces(hovertemplate = hover.clustered_barchart_hover_template(fig.data[1].x))
    fig['layout']['xaxis'].update(autorange = True)
    fig.data[1].name = 'Déclarer sans erreurs'
    return fig
