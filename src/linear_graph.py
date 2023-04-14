import plotly.express as px
import hover_template as hover

def get_line_chart_figure(my_df):
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

    return fig

