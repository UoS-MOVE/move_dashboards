"""
Initialize Flask app.
"""


__author__ = "Ethan Bellmer"
__version__ = "0.1"


import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html


def init_dashboard(server):
	"""Create a Plotly Dash dashboard."""
	dash_app = dash.Dash(
		server=server,
		routes_pathname_prefix='/dash/',
		external_stylesheets=[
			'/static/dist/css/styles.css',
		]
	)

	# Create Dash Layout
	dash_app.layout = html.Div(id='dash-container')

	# Initialize callbacks after our app is loaded
	# Pass dash_app as a parameter
	init_callbacks(dash_app)

	return dash_app.server


def init_callbacks(dash_app):
	@app.callback(
	# Callback input/output
	)
	def update_graph(rows):
		# Callback logic