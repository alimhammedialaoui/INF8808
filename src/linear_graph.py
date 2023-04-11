import plotly.express as px

def get_line_chart_figure(my_df):
    fig = px.line(my_df,x="Year", y="Valeurs", color = 'Form_juridique', markers=True)
    return fig
