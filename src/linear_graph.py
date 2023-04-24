import plotly.express as px
import hover_template as hover

def get_line_chart_figure(my_df):
    """
    Generates the linegraph.

    Args:
        my_df: The dataframe to display
    Returns:
        The generated figure
    """
    fig = px.line(my_df,
                  x="Year", 
                  y=round(my_df["Valeurs"]*100,2), 
                  range_y=[0,100],
                  labels={
                        "Year": "Années",
                        "C": "Entreprises",
                        "P": "Particuliers",
                        "S": "Syndicats",
                        "Form_juridique": "Forme juridique"
                    },
                  title = "Évolution de la complétion des déclarations par groupe de contribuable",
                  color = 'Form_juridique', 
                  color_discrete_sequence=px.colors.qualitative.Set1,
                  markers=True)
    fig.update_traces(mode = 'markers+lines', hovertemplate = None)
    fig.update_layout(title_x = 0.5, yaxis_title="% de respect", hovermode = "x unified")
    for index, value in enumerate(fig.data):
      if value.name =='C':
        value.name = 'Entreprise'
      elif value.name =='P':
        value.name = 'Particulier'
      else:
        value.name = 'Syndicat'
        
    fig.update_layout(xaxis_title='')
    fig.add_annotation(x=2013.80, y=-0.17, 
                       xref="x", 
                       yref="paper", 
                       showarrow=False, 
                       text="Années", 
                       font=dict(size=14), 
                       textangle=0)
    
    fig.update_layout(yaxis_title='')
    fig.add_annotation(x=-0.22, y=0.5, 
                       xref="paper", 
                       yref="paper", 
                       showarrow=False, 
                       text="% de respect", 
                       font=dict(size=14), 
                       textangle=0,
                       standoff = 50
                       )
    fig.update_yaxes(title=dict(standoff = 80))
    
    return fig

