import plotly.express as px
import plotly.graph_objects as go
from Levenshtein import distance

import hover_template as hover

dico_conjugaison = {
    'Declarer' : 'déclaré',
    'Produire' : 'produit'
}

def figure_back(df, quebec_data,color):
    """
    Generates the map.

    Args:
        df: The dataframe to display
        quebec_data: The GeoJSON data
    Returns:
        The generated map
    """
    
    goal = color.split('_') 
    title = " Analyse de la proportion de " + goal[1] +" " +dico_conjugaison[goal[0]]

    fig = px.choropleth_mapbox(df, 
                            geojson=quebec_data, color=color,
                            locations="Region", featureidkey="properties.res_nm_reg",
                            center={"lat": 50, "lon": -70},
                            mapbox_style="carto-positron", zoom=2,
                            title = title,
                            opacity = 0.5,
                            labels={color: "Proportion (%) de " +goal[1] +" " +dico_conjugaison[goal[0]] })
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_x = 0.5)
    return fig