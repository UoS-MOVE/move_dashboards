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
import datetime as dt

import pandas as pd
import json

# Import Dash libraries and dependancies
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth 
from dash.dependencies import Input, Output

# Import process scheduler for funning funtions concurrently
from apscheduler.schedulers.background import BackgroundScheduler

# Custom functions
import dbConnect


# Variable declaration
DB_TABLE = "sensorData"
START_DATE = dt.date.now - dt.date.timedelta(days=7)
END_DATE = dt.date.now


# Pull the initial values
sensorNames = pd.read_sql(dbConnect.fetchSensorNames(DB_TABLE))
sensorData = pd.read_sql(dbConnect.fetchData(DB_TABLE, "sensorName", "plotValues", "", START_DATE, END_DATE))




# Temporary user login credentials, to be replaced with SQL server connection
with open(".usrCreds") as f:
	usrCreds = json.load(f)

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash()

# Define the credentials for authorised users using key:value pairs
## Update to use Database connector
auth = dash_auth.BasicAuth(
	app,
	usrCreds
)


app.layout = html.Div(children=[
	html.H1(children='Hello Dash'),

	html.Div(children='''
		Dash: A web application framework for Python.
	'''),

	html.Div(children=[
		html.Label('Sensor Selector'),
			dcc.Dropdown(
				id='sensor-select-dropdown',
				options=[
					{'label': 'Test', 'value': 'NA'},
					{'label': 'Test2', 'value': 'NA2'},
					{'label': 'Test3', 'value': 'NA3'},
					{'label': 'Test4', 'value': 'NA4'}
				]
			),

		dcc.DatePickerRange(
			id='date-picker',
			month_format='YYYY-MM-DD',
			end_date_placeholder_text='YYYY-MM-DD',
			start_date=START_DATE,
			end_date=END_DATE,
		),
	]),


	dcc.Graph(
		id='time-lapse-graph',
		figure={
			'data': [
				{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
				{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
			],
			'layout': {
				'title': 'Dash Data Visualization'
			}
		}
	),
	dcc.Slider(
		id='date-slider',
		min=sensorData['messageDate'].min(),
		max=sensorData['messageDate'].max(),
		value=sensorData['messageDate'].min(),
	)
])


# Callback definitions
@app.callback(
	Output('time-lapse-graph', 'figure'),
	[Input('sensor-select-dropdown', 'value')]
)
def update_figure(selected_date):
	filtered_df = sensorData[sensorData.messageDate == selected_date]



# Define scheduled functions
sched = BackgroundScheduler()

# Fetch sensor names every hour
@sched.scheduled_job('interval', minutes=60)
def timed_job():
	print('This job is run every minute.')
	sensorNames = pd.read_sql(dbConnect.fetchSensorNames(DB_TABLE))
# Fetch sensor data every 15 minutes from the database
@sched.scheduled_job('interval', minutes=15)
def timed_job():
	print('This job is run every 15 minutes.')
	sensorData = pd.read_sql(dbConnect.fetchData(DB_TABLE, "sensorName", sensorNames['sensorName'].at[0], START_DATE, END_DATE))

# Start the scheduler
sched.start()


# Main function, starts the server instance and serves the prior content
if __name__ == '__main__':
	app.run_server(debug=True)