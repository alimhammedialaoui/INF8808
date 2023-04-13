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
import bubble_chart
import stacked_barchart
import linear_graph

import pandas as pd
import numpy as np
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
years.insert(0,"Tout")

modes_transmission = list(data["Mode_transmission"].dropna().unique())
modes_transmission = list(map(lambda s: s.capitalize(), modes_transmission))
modes_transmission.insert(0,"Tout")

liste_contexte = []
for themes in [
    "Simplifier l'analyse des données fiscales pour les décideurs de Revenu Québec",
    "Réduire les pertes de temps de suivi et de traitement dues aux erreurs de déclaration",
    "Rapidement identifier la conformité fiscale d’un groupe d'individus quant à leur capacité à déclarer dans les temps et produire sans erreurs",
]:
    liste_contexte.append(html.Li(themes))

Particuliers = len(
    data[data["Form_juridique"] == "P"].groupby("Num_contribuable").count()
)
Entreprises = len(
    data[data["Form_juridique"] == "C"].groupby("Num_contribuable").count()
)
Syndicats = len(data[data["Form_juridique"] == "S"].groupby("Num_contribuable").count())

Effectif = len(data["Num_contribuable"].unique())
Timeline = (
    "Données recensées de "
    + str(int(data["Year"].dropna().unique()[0]))
    + " à "
    + str(int(data["Year"].dropna().unique()[-1]))
)
regions = list(data["Region"].dropna().unique())
regions = list(map(lambda s: s.capitalize(), regions))
regions.insert(0,"Tout")
Nb_regions = len(regions)

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

# bubble_chart_pd = yassine_preprocess.bubble_processing(data_whole)
bubble_data = yassine_preprocess.filter_bubble_data(
    data_whole, years[0], modes_transmission[0], formes_juridiques[0], regions[0]
)
bubble_chart_fig = bubble_chart.get_plot(bubble_data)
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

clustered_barchart_fig = clustered_barchart.init_figure()
clustered_barchart_fig = clustered_barchart.draw_clustered_barchart(
    clustered_barchart_fig, data_barchart
)
# fig.update_layout(height=600, width=1200)
clustered_barchart_fig.update_layout(dragmode=False)

indicateurs = ["TVQ", "RAS", "IC", "IP"]
obligations = ["Declarer", "Produire"]
# Preprocess data to create the stacked barchart tab
data_stacked_bchart = preprocess.create_dataset_stacked_barchart(
    data_whole,
    {"Mode_transmission": modes_transmission[0], "Region": regions[0]},
    obligation=obligations[0],
    indicateur=indicateurs[0],
)
stacked_barchart_fig = stacked_barchart.init_figure()
stacked_barchart_fig = stacked_barchart.draw_stacked_barchart(
    stacked_barchart_fig, data_stacked_bchart
)

# Preprocess data to create the line chart figure
line_chart_data = preprocess.filter_line_chart_df(
    data_whole, regions[0], obligations[0], indicateurs[0], modes_transmission[0]
)

line_chart_fig = linear_graph.get_line_chart_figure(line_chart_data)

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
                    style={
                        "font-size": "14px",
                        "height": "4rem",
                        "line-height": "1.5rem",
                    },
                    children=[
                        dcc.Tab(label="Clustered bar chart", value="graph-1"),
                        dcc.Tab(label="Bubble chart", value="graph-2"),
                        dcc.Tab(label="Map", value="graph-3"),
                        dcc.Tab(label="Stacked bar chart", value="graph-4"),
                        dcc.Tab(label="Line graph", value="graph-5"),
                    ],
                ),
                # Zone d'affichage des graphiques
                html.Div(id="graph-display", className="mt-5"),
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
                                                            children=[
                                                                html.P(
                                                                    "Contexte et objectif : "
                                                                ),
                                                                html.Ul(liste_contexte),
                                                                html.P(
                                                                    "Le tableau de bord propose donc une série de 5 visualisations avec un cadre de contrôle pour explorer les différentes modalités des variables."
                                                                ),
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
                                                            children=[
                                                                "Effectif détaillé"
                                                            ],
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


def filter_template_1(figure_input, **kwargs):
    return html.Div(
        className="container",
        children=[
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="col-sm-3 d-flex flex-column justify-content-center",
                        children=[
                            html.Div(className="mb-3", children=["Filters"]),
                            html.Div(
                                className="alabaster p-3",
                                children=[
                                    html.Label(
                                        htmlFor="radio-items_1",
                                        id="mode",
                                        children=["Mode"],
                                        className="font-size-15",
                                        style={"display": kwargs["mode"]},
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
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["mode"],
                                                },
                                            )
                                        ],
                                    ),
                                    html.Label(
                                        htmlFor="radio-items_2",
                                        id="annee",
                                        children=["Année"],
                                        className="font-size-15",
                                        style={"display": kwargs["year"]},
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="radio-items_2",
                                                options=years,
                                                value=years[0],
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["year"],
                                                },
                                            )
                                        ],
                                    ),
                                    html.Label(
                                        htmlFor="radio-items_3",
                                        id="forme_juridique",
                                        children=["Forme juridique"],
                                        className="font-size-15",
                                        style={"display": kwargs["forme"]},
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="radio-items_3",
                                                options=formes_juridiques,
                                                value=formes_juridiques[0],
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["forme"],
                                                },
                                            )
                                        ],
                                    ),
                                    html.Label(
                                        htmlFor="radio-items_4",
                                        id="transmission",
                                        children=["Transmission"],
                                        className="font-size-15",
                                        style={"display": kwargs["trans"]},
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="radio-items_4",
                                                options=modes_transmission,
                                                value=modes_transmission[0],
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["trans"],
                                                },
                                            )
                                        ],
                                    ),
                                    html.Label(
                                        htmlFor="radio-items_5",
                                        id="region",
                                        children=["Region"],
                                        className="font-size-15",
                                        style={"display": kwargs["region"]},
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="radio-items_5",
                                                options=regions,
                                                value=regions[0],
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["region"],
                                                },
                                            )
                                        ],
                                    ),
                                    html.Label(
                                        htmlFor="radio-items_6",
                                        id="indicateur",
                                        children=["Indicateur"],
                                        className="font-size-15",
                                        style={"display": kwargs["indicateur"]},
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="radio-items_6",
                                                options=indicateurs,
                                                value=indicateurs[0],
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["indicateur"],
                                                },
                                            )
                                        ],
                                    ),
                                    html.Label(
                                        htmlFor="radio-items_7",
                                        id="obligation",
                                        children=["Obligation"],
                                        className="font-size-15",
                                        style={"display": kwargs["obligation"]},
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id="radio-items_7",
                                                options=obligations,
                                                value=obligations[0],
                                                clearable=False,
                                                style={
                                                    "whiteSpace": "nowrap",
                                                    "fontSize": "14px",
                                                    "display": kwargs["obligation"],
                                                },
                                            )
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="col-sm-9",
                        children=[
                            dcc.Graph(
                                figure=figure_input,
                                id="out-plot",
                                config=dict(doubleClick="autoscale"),
                            )
                        ],
                    ),
                ],
            )
        ],
    )


YASSINE_FIG = bubble_chart_fig

BASTA_FIG = clustered_barchart_fig

PIERRE_FIG = stacked_barchart_fig

UGO_FIG = line_chart_fig

BASTA_HTML = filter_template_1(
    BASTA_FIG,
    mode="",
    year="",
    trans="",
    forme="",
    region="none",
    obligation="none",
    indicateur="none",
)
YASSINE_HTML = filter_template_1(
    YASSINE_FIG,
    mode="none",
    year="",
    trans="",
    forme="",
    region="",
    obligation="none",
    indicateur="none",
)

PIERRE_HTML = filter_template_1(
    PIERRE_FIG,
    mode="none",
    year="none",
    trans="",
    forme="",
    region="none",
    obligation="",
    indicateur="",
)

UGO_HTML = filter_template_1(
    UGO_FIG,
    mode="none",
    year="none",
    trans="",
    forme="none",
    region="",
    obligation="",
    indicateur="",
)


@app.callback(
    Output("out-plot", "figure"),
    [
        Input("tabs", "value"),
        Input("radio-items_1", "value"),
        Input("radio-items_2", "value"),
        Input("radio-items_3", "value"),
        Input("radio-items_4", "value"),
        Input("radio-items_5", "value"),
        Input("radio-items_6", "value"),
        Input("radio-items_7", "value"),
    ],
)
def filter_plot(
    tab, mode, year, forme_juridique, mode_transmission, region, indicateur, obligation
):
    """
    Updates the application after the filter has changed

    Args:
        mode: The mode selected.
        figure: The figure as it is currently displayed
    Returns:
        fig: The figure to display after the change of radio input
        mode: The new mode
    """
    if tab == "graph-1":
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
    elif tab == "graph-2":
        bubble_data = yassine_preprocess.filter_bubble_data(
            data_whole, year, mode_transmission, forme_juridique, region
        )
        fig = bubble_chart.get_plot(bubble_data)
    elif tab == "graph-4":
        stacked_data = preprocess.create_dataset_stacked_barchart(
            data_whole,
            {"Mode_transmission": mode_transmission, "Region": region},
            obligation=obligation,
            indicateur=indicateur,
        )
        fig = stacked_barchart.init_figure()
        fig = stacked_barchart.draw_stacked_barchart(stacked_barchart_fig, stacked_data)
    elif tab=="graph-5":
        line_chart_data = preprocess.filter_line_chart_df(
            data_whole, region, obligation, indicateur, mode_transmission
        )

        fig = linear_graph.get_line_chart_figure(line_chart_data)
    # fig.update_layout(height=600, width=1200)
    fig.update_layout(dragmode=False)
    return fig


@app.callback(
    [Output("plot-container", "className"), Output("homepage", "className")],
    [Input("show-dashboard-button", "n_clicks"), Input("previous-button", "n_clicks")],
)
def show_plot(n_clicks_1, n_clicks_2):
    # print("Show ", n_clicks_1, ", Previous ", n_clicks_2)
    if n_clicks_1 == n_clicks_2:
        return "hide", "lead"
    else:
        return "lead", "hide"


@app.callback(Output("graph-display", "children"), Input("tabs", "value"))
def display_graph(value):
    if value == "graph-1":
        return BASTA_HTML
    elif value == "graph-2":
        return YASSINE_HTML
    elif value == "graph-3":
        return BASTA_HTML
    elif value == "graph-4":
        return PIERRE_HTML
    elif value == "graph-5":
        return UGO_HTML


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
