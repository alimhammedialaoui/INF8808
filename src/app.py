
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Course: Projet INF8808 - Groupe 10 
    Python Version: 3.8

    This file contains the source code for the project.
'''
import json

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd

import preprocess
import clustered_barchart
import stacked_barchart


app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

data = pd.read_csv('assets/dataset.csv', delimiter=";", encoding='latin-1')

    
print("Lecture fichier ok")

data_IC = data[data['Form_juridique'] == 'C']
data_IP = data[data['Form_juridique'] == 'P']

data_IC = preprocess.clean_names(data_IC)
data_IC = preprocess.remove_missing_values(data_IC, 'IC')
data_IC = preprocess.convert_types(data_IC, 'IC')
data_IC = preprocess.sort_by_yr(data_IC)

data_IP = preprocess.clean_names(data_IP)
data_IP = preprocess.remove_missing_values(data_IP, 'IP')
data_IP = preprocess.convert_types(data_IP, 'IP')
data_IP = preprocess.sort_by_yr(data_IP)

data_whole = preprocess.combine_dfs(data_IC,data_IP)

# Exemple d'application du groupement 
data_mean_by_year_and_region = preprocess.group_and_get_means_per_obligation(['Year', 'Region'], data_whole)
data_sum_by_year_and_region = preprocess.group_and_get_means_per_obligation(['Year', 'Region'], data_whole)

data_mean_by_year = preprocess.group_and_get_means_per_obligation(['Year'], data_whole)

# Preprocess data to create the clustered barchart tab
data_barchart = preprocess.create_dataset_clustered_barchart({'Year':2014}, data_mean_by_year)

# Preprocess data to create the stacked barchart tab
data_stacked_bchart = preprocess.create_dataset_stacked_barchart(data_whole, {'Mode_transmission': 'Logiciel', 'Region': 'Lanaudiere'}, obligation='Declarer', indicateur='TVQ')

fig = clustered_barchart.init_figure()
fig = clustered_barchart.draw_clustered_barchart(fig, data_barchart)
#fig = stacked_barchart.init_figure()
#fig = stacked_barchart.draw_stacked_barchart(fig, data_stacked_bchart)
fig.update_layout(height=600, width=1200)
fig.update_layout(dragmode=False)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Analyse des obligations applicables à quatre lois fiscales en vigueur au Québec', style={'textAlign': 'center'}),
        html.H2('Présentation du site', style={'textAlign': 'center'})
    ]),
    html.Main(className='viz-container', children=[
                                            dcc.Graph(className='graph', figure=fig, config=dict(
                                                doubleClick='autoscale'
                                                ),
                                                id = 'bar-chart')
                                            ],
              style={'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                    'width': '60%'
                    }), 
    html.Footer(children=[
            html.Div(className='panel', children=[
                html.Div(id='info', children=[
                    html.P("Utilisez le bouton pour changer l'affichage", style={'textAlign': 'center'}),
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
                style={'textAlign':'center'
                    })
])

@app.callback(
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
    data_barchart = preprocess.create_dataset_clustered_barchart({'Year':2014}, data_mean_by_year, radio_fusion = mode)
    fig = clustered_barchart.draw_clustered_barchart(fig, data_barchart)
    fig.update_layout(height=600, width=1200)
    fig.update_layout(dragmode=False)
    return fig, mode
