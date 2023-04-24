
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Course: Projet INF8808 - Groupe 10
    Python Version: 3.8

    This file contains the source code for the project.
'''
import json

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd

import preprocess
import clustered_barchart
import stacked_barchart

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Projet | INF8808'

data = pd.read_csv('assets/dataset.csv', delimiter=";", encoding='latin-1')


print("Lecture fichier ok")

data_IC = data[data['Form_juridique'] == 'C']
data_IP = data[data['Form_juridique'] == 'P']
data_S = data[data['Form_juridique'] == 'S']

data_IC = preprocess.clean_names(data_IC)
data_IC = preprocess.remove_missing_values(data_IC, 'IC')
data_IC = preprocess.convert_types(data_IC, 'IC')
data_IC = preprocess.sort_by_yr(data_IC)

data_IP = preprocess.clean_names(data_IP)
data_IP = preprocess.remove_missing_values(data_IP, 'IP')
data_IP = preprocess.convert_types(data_IP, 'IP')
data_IP = preprocess.sort_by_yr(data_IP)

data_S = preprocess.clean_names(data_S)
data_S = preprocess.remove_missing_values(data_S, None)
data_S = preprocess.convert_types(data_S, None)
data_S = preprocess.sort_by_yr(data_S)


data_whole = preprocess.combine_dfs(data_IC,data_IP, data_S)
data_whole = preprocess.combine_dfs(data_IC, data_IP)

# Exemple d'application du groupement
data_mean_by_year_and_region = preprocess.group_and_get_means_per_obligation(['Year', 'Region'], data_whole)
data_sum_by_year_and_region = preprocess.group_and_get_means_per_obligation(['Year', 'Region'], data_whole)
# Exemple d'application du groupement
data_mean_by_year_and_region = preprocess.group_and_get_means_per_obligation(
    ['Year', 'Region'], data_whole)
data_sum_by_year_and_region = preprocess.group_and_get_means_per_obligation(
    ['Year', 'Region'], data_whole)

data_mean_by_year = preprocess.group_and_get_means_per_obligation([
                                                                  'Year'], data_whole)

# Preprocess data to create the clustered barchart tab
data_barchart = preprocess.create_dataset_clustered_barchart({'Year':2014}, data_mean_by_year)

# Preprocess data to create the stacked barchart tab
data_stacked_bchart = preprocess.create_dataset_stacked_barchart(data_whole, {'Mode_transmission': 'Logiciel', 'Region': 'Lanaudiere'}, obligation='Declarer', indicateur='TVQ')

fig = clustered_barchart.init_figure()
fig = clustered_barchart.draw_clustered_barchart(fig, data_barchart)

fig.update_layout(height=600, width=1200)
fig.update_layout(dragmode=False)


DASHBOARD = html.Div(className="hide",
                     style={'display': 'flex', 'align-items': 'center',
                            'justify-content': 'center', 'height': '100vh'},
                     children=[
                         html.Div(
                             children=[
                                 # Back button with logo
                                 html.Button(id="previous-button", n_clicks=0, children=[
                                     html.Img(
                                         src='https://img.icons8.com/external-outline-stroke-bomsymbols-/91/000000/external-arrow-digital-design-outline-set-2-outline-stroke-bomsymbols-.png',
                                         height='10px', width="auto"),
                                     html.Div("Previous")
                                 ], className="btn arctic-blue"),
                                 # Barre horizontale pour changer entre les graphiques
                                 dcc.Tabs(id='tabs', value='graph-1', children=[
                                     dcc.Tab(label='Clustered bar chart 1',
                                             value='graph-1'),
                                     dcc.Tab(label='Clustered bar chart 2',
                                             value='graph-2'),
                                     dcc.Tab(label='Bubble chart',
                                             value='graph-3'),
                                     dcc.Tab(label='Map',
                                             value='graph-4'),
                                     dcc.Tab(label='Stacked bar chart',
                                             value='graph-5'),
                                     dcc.Tab(label='Line graph',
                                             value='graph-6'),
                                 ]),
                                 # Zone d'affichage des graphiques
                                 html.Div(id='graph-display')
                             ]
                         )
                     ]
                     )


app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Analyse des obligations applicables à quatre lois fiscales en vigueur au Québec'),
        # html.H2('Présentation du site', style={'textAlign': 'center'})
    ]),
    html.Div(id="homepage", className="wrapper", children=[
        html.Div(className="box a rose-red", children=[
            html.Span("Le projet vise à simplifier l'analyse des données fiscales pour les décideurs de Revenu Québec. En effet, les erreurs de déclaration entraînent des suivis et engendrent des pertes de temps que l'on veut réduire au maximum. L'objectif principal de ce tableau de bord est de rapidement identifier la conformité fiscale d’un groupe d'individus quant à leur capacité à déclarer dans les temps et produire sans erreurs.\n Le tableau de bord propose donc une série de 5 visualisations avec un cadre de contrôle pour explorer les différentes modalités des variables.",
                      className="text white-text")
        ]),
        html.Div(className="box b arctic-blue", children=[
            html.Div(className="container", children=[
                html.Div(className="col", children=[
                    html.Div(html.Img(
                        src='https://img.icons8.com/color/48/null/conference-call--v1.png', height="60px")),
                    html.Div("X particuliers")
                ]),
                html.Div(className="col", children=[
                    html.Div(html.Img(
                        src='https://img.icons8.com/fluency/48/null/organization-chart-people.png', height="60px")),
                    html.Div("Y entreprises")
                ]),
                html.Div(className="col", children=[
                    html.Div(html.Img(
                        src='https://img.icons8.com/fluency/48/null/security-user-male.png', height="60px")),
                    html.Div("Z syndicats")
                ])
            ])
        ]),
        html.Div(className="box c dark-cyan ", children=[
            html.Button(className="white-text btn", children=['Accès au tableau de bord'],
                        id='show-dashboard-button', n_clicks=0, style={'width': '100%', 'border-radius': '10px', 'height': '100%'})]),
        html.Div(className="box d arctic-blue", children=[
            html.Div(className="container-col", children=[
                html.Div(className="row", children=[
                    html.Div(html.Img(
                        src='https://img.icons8.com/fluency/48/000000/time.png', height="60px")),
                    html.Div("XX déclarations non déclarées à temps")
                ]),
                html.Div(className="row", children=[
                    html.Div(html.Img(
                        src='https://img.icons8.com/fluency/48/null/fingerprint-error.png', height="60px")),
                    html.Div("XY déclarations avec des erreurs")
                ]),
            ])
        ])
    ]),
    # Container for the plot
    html.Div(id='plot-container', children=[DASHBOARD])
])


BASTA_HTML = html.Main(className='viz-container', children=[
    dcc.Graph(className='graph', figure=fig, config=dict(
        doubleClick='autoscale'
    ), id='bar-chart')
], style={'display': 'flex', 'align-items': 'center',
          'justify-content': 'center',
          'margin-left': 'auto',
          'margin-right': 'auto',
          'width': '60%'
          }),\
    html.Footer(children=[
        html.Div(className='panel', children=[
            html.Div(id='info', children=[
                        html.P("Utilisez le bouton pour changer l'affichage",
                               style={'textAlign': 'center'}),
                        html.P(html.Span('', id='mode')
                               )
            ]),
            html.Div(children=[
                dcc.RadioItems(
                    id='radio-items',
                    options=[
                        dict(
                            label='Obligations par lois fiscales',
                            value=False),
                        dict(
                            label='Grouper les lois par obligations fiscales',
                            value=True),
                    ],
                    value=False
                )
            ])
        ])
    ],
        style={'textAlign': 'center'})


@ app.callback(
    [Output('bar-chart', 'figure'), Output('mode', 'children')],
    [Input('radio-items', 'value')],
    [State('bar-chart', 'figure')]
)
def radio_updated(mode, figure):
    '''
        Updates the application after the radio input is modified.
    
        Args:
            mode: The mode selected in the radio input.
            figure: The figure as it is currently displayed
        Returns:
            fig: The figure to display after the change of radio input
            mode: The new mode
    '''
    fig = clustered_barchart.init_figure()
    data_barchart = preprocess.create_dataset_clustered_barchart(
        {'Year': 2014}, data_mean_by_year, radio_fusion=mode)
    fig = clustered_barchart.draw_clustered_barchart(fig, data_barchart)
    fig.update_layout(height=600, width=1200)
    fig.update_layout(dragmode=False)
    return fig, mode


@ app.callback([Output('plot-container', 'className'), Output('homepage', 'className')],
               [Input('show-dashboard-button', 'n_clicks'), Input('previous-button', 'n_clicks')])
def show_plot(n_clicks_1, n_clicks_2):
    print("Show ", n_clicks_1, ", Previous ", n_clicks_2)
    if n_clicks_1 == n_clicks_2:
        return "hide", "wrapper"
    else:
        return None, "hide"


@ app.callback(Output('graph-display', 'children'),
               [Input('tabs', 'value')])
def display_graph(value):
    if value == 'graph-1':
        return BASTA_HTML
    elif value == 'graph-2':
        return BASTA_HTML
    elif value == 'graph-3':
        return BASTA_HTML
    elif value == 'graph-4':
        return BASTA_HTML
    elif value == 'graph-5':
        return BASTA_HTML
    elif value == 'graph-6':
        return BASTA_HTML
