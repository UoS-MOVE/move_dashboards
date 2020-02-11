# Title: Plotly Dash Dashboard for MOVE
# Description: Dashboard implementation for the sensors installed 
# 				in the Slaford Museum and Art Gallery using Plotly's Dash system
# Author: Ethan Bellmer
# Date: 06.02.2020
# Version: 0.1

# Venv activation is blocked by default because the process isn't singed, so run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process


# Library imports
import os
import pyodbc
import traceback 

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth 

import json 

# Custom functions
import dbConnect


# Temporary user login credentials
#SQL Server connection info
with open(".usrCreds") as f:
	usrCreds = json.load(f)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    usrCreds
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)