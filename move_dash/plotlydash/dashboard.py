"""Instantiate a Dash app."""
from os import name
import numpy as np
import pandas as pd
import dash
from dash import dash_table
from dash import html
from dash import dcc
import plotly.graph_objects as go
from .data import create_dataframe, get_monnit_data
from .layout import html_layout


def init_dashboard(server):
	"""Create a Plotly Dash dashboard."""
	dash_app = dash.Dash(
		server=server,
		routes_pathname_prefix='/dashapp/',
		external_stylesheets=[
			'/static/dist/css/styles.css',
			'https://fonts.googleapis.com/css?family=Lato'
		]
	)

	# Load DataFrame
	df = create_dataframe()

	# Custom HTML layout
	dash_app.index_string = html_layout



	def graph_scatter(sensor_name):
		df = get_monnit_data(sensor_name)
		X = df['messageDate']
		Y = df['plotValue']

		data = go.Scatter(
				x=list(X),
				y=list(Y),
				name=sensor_name,
				mode= 'lines+markers'
				)

		return {'data': [data],'layout' : go.Layout(
									title=sensor_name,)}


	# Create Layout
	dash_app.layout = html.Div(
		children=[
			dcc.Graph(id='498873', figure= graph_scatter('Tem - Z03 - Top West (South Rail) - 498873')),
			dcc.Graph(id='498886', figure= graph_scatter('Tem - Z03 - Bottom East - 498886')),
			dcc.Graph(id='498884', figure= graph_scatter('Tem - Z03 - Top West (North Rail) - 498884')),
			dcc.Graph(id='498880', figure= graph_scatter('Tem - Z03 - Bottom West - 498880'))
		],
		id='dash-container'
	)
	return dash_app.server


def create_data_table(df):
	"""Create Dash datatable from Pandas DataFrame."""
	table = dash_table.DataTable(
		id='database-table',
		columns=[{"name": i, "id": i} for i in df.columns],
		data=df.to_dict('records'),
		sort_action="native",
		sort_mode='native',
		page_size=300
	)
	return table