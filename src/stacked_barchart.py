'''
    Contains some functions related to the creation of the stacked bar chart

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

def draw_stacked_barchart(fig, data, scale_mode):
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
    fig.data = []
    range_y=[0,100]
    
    """ fig = px.bar(data,
                 x ="Year",
                 y = "Valeurs",
                 range_y=range_y,
                 color="Taille",
                 labels={
                        "Valeurs": "% de respect de l'obligation",
                        "Year": "Années",
                        'Taille': "Taille de l'entreprise"
                    },
                 title = "Évolution sur la complétion des déclarations par type d'entreprise",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 custom_data=["Tot_par_taille", "Tot"],
                )
    fig.update_layout(title_x = 0.5) """

    tailles = data["Taille"].unique()
    #print(list(tailles))
    for i, taille in enumerate(tailles):
        curr_data=data[data["Taille"] == taille]
        color = px.colors.qualitative.Set1[i]
        traces = create_bar_traces(curr_data, color, taille)
        fig.add_traces(traces[0])
        fig.add_traces(traces[1])
    """ data_grande= data[data["Taille"] == "Grande"]
    data_moyenne = data[data["Taille"] == "Moyenne"]
    data_petite= data[data["Taille"] == "Petite"]
    trace_grande = go.Bar(x=data_grande["Year"], y=data_grande["Tot_par_taille"])
    trace_moyenne = go.Bar()
    trace_petite = go.Bar(x=data_petite["Year"], 
                          y=data_petite["Tot_par_taille"]-data_petite["Valeurs"], 
                          marker_color=px.colors.qualitative.Set1[2], 
                          opacity=0.4, 
                          customdata=data_petite[["Tot_par_taille", "Tot"]]) """

    fig.update_yaxes(type='linear')
    if scale_mode:
        range_y = [0, 2]
        fig.update_yaxes(type='log')

    fig.update_layout(yaxis_range=range_y)
    fig.update_layout(legend_title_text="Taille d'entreprise et respect")

    fig.update_traces(hovertemplate = hover.stacked_barchart_hover_template())

    return fig

def create_bar_traces(data, color, name):
    trace1 = go.Bar(x=data["Year"], 
                    y=data["Valeurs"],
                    marker_color=color,
                    customdata=data[["Tot_par_taille", "Tot"]],
                    name=name + ", respecte")
    trace2 = go.Bar(x=data["Year"], 
                    y=data["Tot_par_taille"]-data["Valeurs"],
                    marker_color=color, 
                    opacity=0.4, 
                    customdata=data[["Tot_par_taille", "Tot"]],
                    name=name + ", ne respecte pas",
                    )
    return trace1, trace2