# -*- coding: utf-8 -*-

"""
    File name: app.py
    Course: Projet INF8808 - Groupe 10
    Python Version: 3.8

    This file contains the source code for the project.
"""
import json

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import yassine_preprocess

import pandas as pd

import preprocess
import clustered_barchart

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=[dbc.icons.FONT_AWESOME])
app.title = "Projet | INF8808"

data = pd.read_csv("assets/dataset.csv", delimiter=";", encoding="latin-1")

formes_juridiques = data["Form_juridique"].dropna().unique()

years = list(data["Year"].dropna().unique())
years = list(map(lambda x: int(x), years))
years.sort()

modes_transmission = list(data["Mode_transmission"].dropna().unique())
modes_transmission = list(map(lambda s: s.capitalize(), modes_transmission))

liste_contexte = []
for themes in ["Simplifier l'analyse des données fiscales pour les décideurs de Revenu Québec",
               "Réduire les pertes de temps de suivi et de traitement dues aux erreurs de déclaration",
               "Rapidement identifier la conformité fiscale d’un groupe d'individus quant à leur capacité à déclarer dans les temps et produire sans erreurs"]:
    liste_contexte.append(html.Li(themes))

Particuliers = len(data[data["Form_juridique"] == 'P'].groupby('Num_contribuable').count())
Entreprises = len(data[data["Form_juridique"] == 'C'].groupby('Num_contribuable').count()) 
Syndicats = len(data[data["Form_juridique"] == 'S'].groupby('Num_contribuable').count())

Effectif = len(data['Num_contribuable'].unique())
Timeline = "Données recensées de " + str(int(data['Year'].dropna().unique()[0])) + " à " + str(int(data['Year'].dropna().unique()[-1]))
Nb_regions = len(data['Region'].unique())

print("Lecture fichier ok")

data_IC = data[data["Form_juridique"] == "C"]
data_IP = data[data["Form_juridique"] == "P"]
data_S = data[data["Form_juridique"] == "S"]

data_IC = preprocess.clean_names(data_IC)
data_IC = preprocess.remove_missing_values(data_IC, "IC")
data_IC = preprocess.convert_types(data_IC, "IC")
data_IC = preprocess.sort_by_yr(data_IC)

data_IP = preprocess.clean_names(data_IP)
data_IP = preprocess.remove_missing_values(data_IP, "IP")
data_IP = preprocess.convert_types(data_IP, "IP")
data_IP = preprocess.sort_by_yr(data_IP)

data_S = preprocess.clean_names(data_S)
data_S = preprocess.remove_missing_values(data_S, None)
data_S = preprocess.convert_types(data_S, None)
data_S = preprocess.sort_by_yr(data_S)

data_whole = preprocess.combine_dfs(data_IC, data_IP, data_S)

bubble_chart_pd = yassine_preprocess.bubble_processing(data_whole)

# Exemple d'application du groupement

data_mean_by_year_and_region = preprocess.group_and_get_means_per_obligation(
    ["Year", "Region"], data_whole
)

data_sum_by_year_and_region = preprocess.group_and_get_means_per_obligation(
    ["Year", "Region"], data_whole
)

data_mean_by_year = preprocess.group_and_get_means_per_obligation(
    ["Year", "Form_juridique", "Mode_transmission"], data_whole
)

# print(data_mean_by_year)
# import numpy as np
# print(list(np.concatenate([data_mean_by_year.loc[:, data_mean_by_year.columns != 'Year'].values[0], data_mean_by_year.loc[:, data_mean_by_year.columns != 'Year'].values[0]])))

data_barchart = preprocess.create_dataset_clustered_barchart(
    {
        "Year": years[0],
        "Form_juridique": formes_juridiques[0],
        "Mode_transmission": modes_transmission[0],
    },
    data_mean_by_year,
)
# print("Data whole Done")


# print(data_barchart)

fig = clustered_barchart.init_figure()
fig = clustered_barchart.draw_clustered_barchart(fig, data_barchart)
# fig.update_layout(height=600, width=1200)
fig.update_layout(dragmode=False)


DASHBOARD = html.Div(
    className="pb-5 pl-5 pr-5 pt-0",
    children=[
        html.Div(
            children=[
                # Back button with logo
                dbc.Button(
                    id="previous-button",
                    n_clicks=0,
                    children=[
                        html.Div(className="fas fa-caret-left mr-1"),
                        html.Span("Previous"),
                    ],
                    className="btn btn-primary mb-2",
                ),
                # Barre horizontale pour changer entre les graphiques
                dcc.Tabs(
                    id="tabs",
                    value="graph-1",
                    children=[
                        dcc.Tab(label="Clustered bar chart", value="graph-1"),
                        dcc.Tab(label="Bubble chart", value="graph-2"),
                        dcc.Tab(label="Map", value="graph-3"),
                        dcc.Tab(label="Stacked bar chart", value="graph-4"),
                        dcc.Tab(label="Line graph", value="graph-5"),
                    ],
                ),
                # Zone d'affichage des graphiques
                html.Div(id="graph-display"),
            ]
        )
    ],
)

app.layout = html.Div(
    children=[
        html.Div(
            className="jumbotron",
            children=[
                html.H1(className="display-4", children=["Revenu Quebéc"]),
                html.P(
                    className="lead",
                    children=[
                        "Analyse des obligations applicables à quatre lois fiscales en vigueur au Québec"
                    ],
                ),
                html.Hr(className="my-4"),
            ],
        ),
        html.Div(
            children=[
                html.P(
                    className="lead",
                    id="homepage",
                    children=[
                        # html.A(className="btn btn-primary btn-lg",href="#",role="button",children=["Click here"])
                        html.Div(
                            className="row d-flex justify-content-center",
                            children=[
                                html.Div(
                                    className="card-deck col-md-9 mb-3",
                                    children=[
                                        html.Div(
                                            className="card rose-red white-text",
                                            children=[
                                                html.Div(
                                                    className="card-body",
                                                    children=[
                                                        html.Div(
                                                            className="card-text",
                                                            children=[html.P("Contexte et objectif : "), html.Ul(liste_contexte),
                                                            html.P("Le tableau de bord propose donc une série de 5 visualisations avec un cadre de contrôle pour explorer les différentes modalités des variables."),
                                                                
                                                            ],
                                                        )
                                                    ],
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="card arctic-blue",
                                            children=[
                                                html.Div(
                                                    className="card-body",
                                                    children=[
                                                        html.Div(
                                                            className="row align-items-center mb-5",
                                                            children=[
                                                                html.Div(
                                                                    className="col-sm-2",
                                                                    children=[
                                                                        html.Img(
                                                                            src="https://img.icons8.com/color/72/null/calendar--v1.png"
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-sm-10",
                                                                    children=[
                                                                        html.Small(
                                                                            f"{Timeline}"
                                                                        )
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="row align-items-center mb-5",
                                                            children=[
                                                                html.Div(
                                                                    className="col-sm-2",
                                                                    children=[
                                                                        html.Img(
                                                                            src="https://img.icons8.com/color/72/null/conference-call--v1.png"
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-sm-10",
                                                                    children=[
                                                                        html.Small(
                                                                            f"{Effectif} contribuables"
                                                                        )
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="row align-items-center mb-3",
                                                            children=[
                                                                html.Div(
                                                                    className="col-sm-2",
                                                                    children=[
                                                                        html.Img(
                                                                            src="https://img.icons8.com/office/72/null/country.png"
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-sm-10",
                                                                    children=[
                                                                        html.Small(
                                                                            f"{Nb_regions} régions différentes"
                                                                        )
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(className="w-100"),
                                html.Div(
                                    className="card-deck col-md-9",
                                    children=[
                                        html.Div(
                                            className="card arctic-blue",
                                            children=[
                                                html.Div(
                                                    className="card-body align-items-center justify-content-center",
                                                    children=[
                                                        html.Div(
                                                            className="card-title",
                                                            children=["Effectif détaillé"],
                                                        ),
                                                        html.Div(
                                                            className="row ",
                                                            children=[
                                                                html.Div(
                                                                    className="col-4 text-center",
                                                                    children=[
                                                                        html.Img(
                                                                            src="https://img.icons8.com/color/48/null/conference-call--v1.png",
                                                                            width="60px",
                                                                        ),
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-4 text-center",
                                                                    children=[
                                                                        html.Img(
                                                                            src="https://img.icons8.com/fluency/48/null/organization-chart-people.png",
                                                                            width="60px",
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-4 text-center",
                                                                    children=[
                                                                        html.Img(
                                                                            src="https://img.icons8.com/fluency/48/null/security-user-male.png",
                                                                            width="60px",
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="w-100"
                                                                ),
                                                                html.Div(
                                                                    className="col-4 text-center",
                                                                    children=[
                                                                        html.Small(
                                                                            f"{Particuliers} particuliers"
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-4 text-center",
                                                                    children=[
                                                                        html.Small(
                                                                            f"{Entreprises} entreprises"
                                                                        )
                                                                    ],
                                                                ),
                                                                html.Div(
                                                                    className="col-4 text-center",
                                                                    children=[
                                                                        html.Small(
                                                                            f"{Syndicats} syndicats"
                                                                        )
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="card arctic-blue",
                                            children=[
                                                html.Img(
                                                    className="card-img-top img-cover",
                                                    height="150px",
                                                    src="https://img.freepik.com/free-vector/gradient-infographic-dashboard-elements-pack_52683-61892.jpg?w=740&t=st=1680490889~exp=1680491489~hmac=cf5d3c52b190d7c5c09019be8b8d4ef49bd17f6dcb4822e68f9ffc4e34af7a54",
                                                ),
                                                html.Div(
                                                    className="card-body",
                                                    children=[
                                                        html.H5(
                                                            className="card-title",
                                                            children=[
                                                                "Tableau de bord"
                                                            ],
                                                        ),
                                                        html.Button(
                                                            className="btn btn-primary",
                                                            id="show-dashboard-button",
                                                            n_clicks=0,
                                                            children=[
                                                                html.Span("Accès"),
                                                                html.Div(
                                                                    className="fas fa-caret-right ml-1"
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ]
        ),
        # Container for the plot
        html.Div(id="plot-container", children=[DASHBOARD]),
    ]
)


BASTA_HTML = html.Div(
    className="container",
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-sm-4 p-3",
                    children=[
                        html.Label(
                            htmlFor="radio-items_1", id="mode", children=["Mode"]
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="radio-items_1",
                                    options=[
                                        {
                                            "label": "Grouper les lois par obligations",
                                            "value": True,
                                        },
                                        {
                                            "label": "Obligations par lois fiscales",
                                            "value": False,
                                        },
                                    ],
                                    value=False,
                                )
                            ],
                        ),
                        html.Label(
                            htmlFor="radio-items_2", id="annee", children=["Année"]
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="radio-items_2",
                                    options=years,
                                    value=years[0],
                                )
                            ],
                        ),
                        html.Label(
                            htmlFor="radio-items_3",
                            id="forme_juridique",
                            children=["Forme juridique"],
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="radio-items_3",
                                    options=formes_juridiques,
                                    value=formes_juridiques[0],
                                )
                            ],
                        ),
                        html.Label(
                            htmlFor="radio-items_4",
                            id="transmission",
                            children=["Transmission"],
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="radio-items_4",
                                    options=modes_transmission,
                                    value=modes_transmission[0],
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="col-sm-8",
                    children=[
                        dcc.Graph(
                            className="graph",
                            figure=fig,
                            config=dict(doubleClick="autoscale"),
                            id="bar-chart",
                        )
                    ],
                ),
            ],
        )
    ],
)


@app.callback(
    Output("bar-chart", "figure"),
    [
        Input("radio-items_1", "value"),
        Input("radio-items_2", "value"),
        Input("radio-items_3", "value"),
        Input("radio-items_4", "value"),
    ],
)
def filter_plot(mode, year, forme_juridique, mode_transmission):
    """
    Updates the application after the radio input is modified.

    Args:
        mode: The mode selected in the radio input.
        figure: The figure as it is currently displayed
    Returns:
        fig: The figure to display after the change of radio input
        mode: The new mode
    """
    fig = clustered_barchart.init_figure()
    data_barchart = preprocess.create_dataset_clustered_barchart(
        {
            "Year": year,
            "Form_juridique": forme_juridique,
            "Mode_transmission": mode_transmission,
        },
        data_mean_by_year,
        radio_fusion=mode,
    )
    fig = clustered_barchart.draw_clustered_barchart(fig, data_barchart)
    # fig.update_layout(height=600, width=1200)
    fig.update_layout(dragmode=False)
    return fig


@app.callback(
    [Output("plot-container", "className"), Output("homepage", "className")],
    [Input("show-dashboard-button", "n_clicks"), Input("previous-button", "n_clicks")],
)
def show_plot(n_clicks_1, n_clicks_2):
    print("Show ", n_clicks_1, ", Previous ", n_clicks_2)
    if n_clicks_1 == n_clicks_2:
        return "hide", "lead"
    else:
        return "lead", "hide"


@app.callback(Output("graph-display", "children"), [Input("tabs", "value")])
def display_graph(value):
    if value == "graph-1":
        return BASTA_HTML
    elif value == "graph-2":
        return BASTA_HTML
    elif value == "graph-3":
        return BASTA_HTML
    elif value == "graph-4":
        return BASTA_HTML
    elif value == "graph-5":
        return BASTA_HTML

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)