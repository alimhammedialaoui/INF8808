
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Course: INF8808
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
app.title = 'Project | INF8808'

with open('../src/assets/dataset.xlsx') as data_file:
    data = pd.read_excel(data_file,index_col=0)

fig = None

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('GDP vs. CO2 emissions'),
        html.H2('In countries around the world')
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
