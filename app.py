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
END_DATE = dt.date.today()
START_DATE = dt.date.today() - dt.timedelta(days=7)


# Pull the initial values
#sensorNames = pd.DataFrame(dbConnect.fetchSensorNames(DB_TABLE))
#sensorData = pd.DataFrame(dbConnect.fetchData(DB_TABLE))
sensorNames = dbConnect.fetchSensorNames(DB_TABLE)
sensorData = dbConnect.fetchData(DB_TABLE)



# Temporary user login credentials, to be replaced with SQL server connection
with open(".usrCreds") as f:
	usrCreds = json.load(f)

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )






#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash()

# Define the credentials for authorised users using key:value pairs
## Update to use Database connector
auth = dash_auth.BasicAuth(
	app,
	usrCreds
)

fig = go.Figure(data = [go.Scatter(x=sensorData.messageDate, y=sensorData.plotValues)])

app.layout = html.Div(children=[
	html.H1(children='Hello Dash'),

	html.Div(children='''
		Dash: A web application framework for Python.
	'''),

	html.Div(children=[
		html.Label('Sensor Selector'),
		dcc.Dropdown(id='sensor-select-dropdown', 
		options=[
			{'label': i, 'value': i} for i in sensorNames.sensorName.unique()
		], 
		multi=True )
		]),

		dcc.DatePickerRange(
			id='date-picker',
			month_format='YYYY-MM-DD',
			end_date_placeholder_text='YYYY-MM-DD',
			start_date=START_DATE,
			end_date=END_DATE,
		),


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
	),


	dcc.Graph(
		id='example-graph-2',
		figure=fig
	),



	html.H4(children='Sensors'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in sensorNames.sensorName.unique()
    ], multi=True, placeholder='Filter by sensor name...'),
    html.Div(id='table-container')
	


])


# Callback definitions
@app.callback(
	Output('time-lapse-graph', 'figure'),
	[Input('sensor-select-dropdown', 'value')]
)
def update_figure(selected_date):
	filtered_df = sensorData[sensorData.messageDate == selected_date]



@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(sensorNames)

    dff = sensorData[sensorNames.sensorName.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)



# Define scheduled functions
sched = BackgroundScheduler()

# Fetch sensor names every hour
@sched.scheduled_job('interval', minutes=60)
def timed_job():
	print('This job is run every minute.')
	#sensorNames = pd.read_sql(dbConnect.fetchSensorNames(DB_TABLE))
# Fetch sensor data every 15 minutes from the database
@sched.scheduled_job('interval', minutes=15)
def timed_job():
	print('This job is run every 15 minutes.')
	#sensorData = pd.read_sql(dbConnect.fetchData(DB_TABLE, "sensorName", sensorNames['sensorName'].at[0], START_DATE, END_DATE))

# Start the scheduler
sched.start()


# Main function, starts the server instance and serves the prior content
if __name__ == '__main__':
	app.run_server(debug=True)