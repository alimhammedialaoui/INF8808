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
                  title = "Évolution sur la complétion des déclarations par groupe d’individus",
                  color = 'Form_juridique', 
                  color_discrete_sequence=px.colors.qualitative.Set1,
                  markers=True)
    fig.update_traces(mode = 'markers+lines', hovertemplate = None)
    fig.update_layout(title_x = 0.5, yaxis_title="% de respect", hovermode = "x unified")

    return fig

