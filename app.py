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
from datetime import date
from datetime import datetime

import pandas as pd
import json

# Import Dash libraries and dependancies
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Import process scheduler for funning funtions concurrently
from apscheduler.schedulers.background import BackgroundScheduler

# Custom functions
import dbConnect

# Imported for debugging in VS Code
import flask

# Variable declaration
DB_TABLE = "sensorData"
END_DATE = date.today()
START_DATE = date.today() - dt.timedelta(days=7)


# Initial data pull from the database for the sensor names and sensor data
sensorNames = dbConnect.fetchSensorNames(DB_TABLE)
#sensorData = dbConnect.fetchData(DB_TABLE)
sensorData = dbConnect.fetchData(DB_TABLE, START_DATE, END_DATE)

# Temporary user login credentials, to be replaced with SQL server connection
with open(".usrCreds") as f:
	usrCreds = json.load(f)


# Define functions 
def generate_table(dataframe, max_rows=1000):
	return html.Table(
		# Header
		[html.Tr([html.Th(col) for col in dataframe.columns])] +

		# Body
		[html.Tr([
			html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
		]) for i in range(min(len(dataframe), max_rows))]
	)


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
f_app = flask.Flask(__name__)
app = dash.Dash(__name__, server=f_app)

# Define the credentials for authorised users using key:value pairs
## Update to use Database connector
auth = dash_auth.BasicAuth(
	app,
	usrCreds
)


app.layout = html.Div(children=[
	
	dcc.Tabs(id="tabs", value='tab-1', children=[
		dcc.Tab(label='Tab one', value='tab-1'),
		dcc.Tab(label='Tab two', value='tab-2'),
		dcc.Tab(label='Tab three', value='tab-3'),
	]),
	html.Div(id='tabs-content'),
	
	html.H1(children='Hello Dash'),

	html.Div(children='''
		Dash: A web application framework for Python.
	'''),

	html.Div(children=[
		# Dropdown selector for the available sensors for the time-series chart
		html.Label('Sensor Selector'),
		dcc.Dropdown(id='sensor-select-dropdown', 
			options=[
				{'label': i, 'value': i} for i in sensorNames.sensorName.unique()
			],
			value = sensorNames.sensorName[4],
			multi=True
		),

		# Date picker for selecting the date range for the data to be pulled from the DB
		dcc.DatePickerRange(
			id='date-picker',
			month_format='YYYY-MM-DD',
			display_format='YYYY-MM-DD',
			end_date_placeholder_text='YYYY-MM-DD',
			start_date=START_DATE,
			end_date=END_DATE,
		),
	]),


	# Time lapse graph to be generated from the aggregated data
	dcc.Graph(
		id='time-lapse-graph',
	),


	dcc.Graph(
		id='bar-graph',
	),

	# Dropdown and table generation for the available sensors
	html.H4(children='Sensor Table'),
	dcc.Dropdown(id='sensor-table-dropdown', options=[
		{'label': i, 'value': i} for i in sensorNames.sensorName.unique()
	], multi=True, placeholder='Filter by sensor name...'),
	html.Div(id='table-container')

])


# Callback definitions
@app.callback(Output('tabs-content', 'children'),
			  [Input('tabs', 'value')])
def render_content(tab):
	if tab == 'tab-1':
		return html.Div([
			html.H3('Tab content 1')
		])
	elif tab == 'tab-2':
		return html.Div([
			html.H3('Tab content 2')
		])
	elif tab == 'tab-3':
		return html.Div([
			html.H3('Tab content 3')
		])

@app.callback(
	Output('time-lapse-graph', 'figure'),
	[Input('sensor-select-dropdown', 'value'),
	#[Input('date-picker', 'value')],
	Input('date-picker', 'start_date'),
	Input('date-picker', 'end_date')]
)
def update_figure(selected_sensor, start_date, end_date):
	#filtered_df = sensorData[sensorData.messageDate > start_date]
	#filtered_df = filtered_df[sensorData.messageDate < end_date]
	
	if isinstance(selected_sensor, str):
		filtered_df = sensorData[sensorData.sensorName == selected_sensor]
	else:
		filtered_df = sensorData[sensorData.sensorName.isin(selected_sensor)]

	# Moved to DB handler
	#filtered_df = filtered_df.sort_values(by='messageDate')


	traces = []
	for i in filtered_df.sensorName.unique():
		df_by_sensor = filtered_df[filtered_df['sensorName'] == i]
		traces.append(dict(
			x=df_by_sensor['messageDate'],
			y=df_by_sensor['plotValues'],
			text=df_by_sensor['sensorName'],
			#mode='markers',
			#opacity=0.7,
			#marker={
			#	'size': 15,
			#	'line': {'width': 0.5, 'color': 'white'}
			#},
			name=i
		))

	return {
		'data': traces,
		'layout': dict(
			title = 'Temperature Data',
			#margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
			#legend={'x': 0, 'y': 1},
			hovermode='closest',
			transition = {'duration': 500},
		)
	}

# Callback for sensor select dropdown
@app.callback(
	dash.dependencies.Output('table-container', 'children'),
	[dash.dependencies.Input('sensor-table-dropdown', 'value')]
)
def display_table(dropdown_value):
	if dropdown_value is None:
		return generate_table(sensorData)

	dff = sensorData[sensorData.sensorName.str.contains('|'.join(dropdown_value))]
	return generate_table(dff)


# Define scheduled functions
sched = BackgroundScheduler()

# Fetch sensor names every hour
@sched.scheduled_job('interval', minutes=60)
def timed_job_60():
	print('(Scheduled Job) This job is run every 60 minutes.')
	sensorNames = dbConnect.fetchSensorNames(DB_TABLE)

# Fetch sensor data every 15 minutes from the database
@sched.scheduled_job('interval', minutes=15)
def timed_job_15():
	print('(Scheduled Job) This job is run every 15 minutes.')
	#sensorData = dbConnect.fetchData(DB_TABLE)
	sensorData = dbConnect.fetchData(DB_TABLE, START_DATE, END_DATE)



# TESTING: Pull sensor data every 30 seconds
#@sched.scheduled_job('interval', seconds=30)
#def timed_job_30():
#	print('(Scheduled Job) This job is run every 30 seconds.')
#	#sensorData = dbConnect.fetchData(DB_TABLE)
#	sensorData = dbConnect.fetchData(DB_TABLE, START_DATE, END_DATE)


# Start the scheduler for the fetch jobs
sched.start()


# Main function, starts the server instance and serves the prior content
if __name__ == '__main__':
	app.run_server(debug=True)