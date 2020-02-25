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


# Variable declaration
DB_TABLE = "sensorData"
END_DATE = date.today()
START_DATE = date.today() - dt.timedelta(days=7)


# Initial data pull from the database fo rthe sensor names and sensor data
sensorNames = dbConnect.fetchSensorNames(DB_TABLE)
sensorData = dbConnect.fetchData(DB_TABLE)


# Temporary user login credentials, to be replaced with SQL server connection
with open(".usrCreds") as f:
	usrCreds = json.load(f)


# Define functions 
def generate_table(dataframe, max_rows=10):
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
app = dash.Dash(__name__)

# Define the credentials for authorised users using key:value pairs
## Update to use Database connector
auth = dash_auth.BasicAuth(
	app,
	usrCreds
)

sens = sensorData[sensorData.sensorName == "Tem - Z03 - Top West (North Rail) - 498884"]
sens.sort_values(by='messageDate', ascending = True, na_position = 'first')
#sens = sensorData
#sens.filter(items = "Tem - Z03 - Top West (North Rail) - 498884", axis = 0)
fig = go.Figure(data = [go.Scatter(x=sens.messageDate, y=sens.plotValues)])

app.layout = html.Div(children=[
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
		value = sensorData.sensorName[4],
		multi=True ),

		# Date picker for selecting the date range for the data to be pulled from the DB
		dcc.DatePickerRange(
			id='date-picker',
			month_format='YYYY-MM-DD',
			display_format='YY, MMM Do',
			end_date_placeholder_text='YYYY-MM-DD',
			start_date=START_DATE,
			end_date=END_DATE,
		),
	]),


	# Time lapse graph to be generated from the aggregated data
	dcc.Graph(
		id='time-lapse-graph',
		#figure=fig
	),

	dcc.Graph(
		id='time-lapse-graph2',
		figure=fig
	),

	# Test slider for experimenting with fine-tuning selected data
	dcc.Slider(
		id='date-slider',
		min=sensorData['messageDate'].min(),
		max=sensorData['messageDate'].max(),
		value=sensorData['messageDate'].min(),
	),


	# Dropdown and table generation for the available sensors
	html.H4(children='Sensor Table'),
	dcc.Dropdown(id='sensor-table-dropdown', options=[
		{'label': i, 'value': i} for i in sensorNames.sensorName.unique()
	], multi=True, placeholder='Filter by sensor name...'),
	html.Div(id='table-container')

])

# page layouts for a multi-page dashboard
layout_page_1 = html.Div([
	html.H4(children='Page 1')
])

layout_page_2 = html.Div([
	html.H4(children='Page 2')
])

# Callback definitions
@app.callback(
	Output('time-lapse-graph', 'figure'),
	[Input('sensor-select-dropdown', 'value')],
	#[Input('date-picker', 'start_date')],
	#[Input('date-picker', 'end_date')]
)
def update_figure(selected_sensor):
	#filtered_df = sensorData[sensorData.messageDate > start_date]
	#filtered_df = filtered_df[sensorData.messageDate < end_date]
	#filtered_df = filtered_df[filtered_df.sensorName == selected_sensor]
	filtered_df = sensorData[sensorData.sensorName == selected_sensor]

	fig = go.Figure(data = [go.Scatter(x=filtered_df.messageDate, y=filtered_df.plotValues)])

	#return fig


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
	print('This job is run every 60 minutes.')
	sensorNames = dbConnect.fetchSensorNames(DB_TABLE)

# Fetch sensor data every 15 minutes from the database
@sched.scheduled_job('interval', minutes=15)
def timed_job_15():
	print('This job is run every 15 minutes.')
	sensorData = dbConnect.fetchData(DB_TABLE)

# Start the scheduler for the fetch jobs
sched.start()


# Main function, starts the server instance and serves the prior content
if __name__ == '__main__':
	app.run_server(debug=True)