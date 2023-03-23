
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

import pandas as pd

import preprocess


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

print(data_mean_by_year_and_region)

fig = None

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Analyse des obligations applicables à quatre lois fiscales en vigueur au Québec'),
        html.H2('Présentation du site')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(className='graph', figure=fig, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
            ))
    ])
])
