'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
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
                 y=data_anim['Valeurs'], 
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 barmode = 'group',
                 #animation_frame=data_anim['Par obligation'],  
                 range_y=[0,1], 
                 color=data_anim['Obligation'],
                 labels={
                        "Valeurs": "% de respect de l'obligation",
                        "Lois": "Lois fiscales",
                        "Obligation": "Obligations fiscales"
                    },
                 title='Analyse de la TVQ, RAS et IP selon les obligations applicables'
                )
    fig.update_layout(title_x = 0.5)
    fig['layout']['xaxis'].update(autorange = True)
    return fig



# def update_animation_menu(fig):
#     '''
#         Updates the animation menu to show the current year, and to remove
#         the unnecessary 'Stop' button.

#         Args:
#             fig: The figure containing the menu to update
#         Returns
#             The updated figure
#     '''
#     # Remove stop button
#     fig['layout']['updatemenus'][0]['buttons'] = [fig['layout']['updatemenus'][0]['buttons'][0]]

#     fig['layout']['sliders'][0]['currentvalue']['prefix'] = 'Par obligation : '
#     fig['layout']['updatemenus'][0]['buttons'][0]['label'] = 'Fusionner'
#     print("1")

#     return fig


# def update_x_axis(fig, mode):
#     '''
#         Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
#         the current display.

#         Args:
#             mode: Current display mode
#         Returns: 
#             The updated figure
#     '''
#     if mode == 'Avec Fusion':
#         fig.update_xaxes(
#             range = [1,8])
#     return fig
