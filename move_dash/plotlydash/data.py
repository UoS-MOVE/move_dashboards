"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd

import pyodbc
from decouple import config


# Batabase access credentials
DB_URL = config('LOCAL_DB_SERVER')
DB_BATABASE = config('LOCAL_DB_DATABASE')
DB_USR = config('LOCAL_DB_USR')
DB_PWD = config('LOCAL_DB_PWD')


def create_dataframe():
	"""Create Pandas DataFrame from local CSV."""
	df = pd.read_csv("data/311-calls.csv", parse_dates=["created"])
	df["created"] = df["created"].dt.date
	df.drop(columns=["incident_zip"], inplace=True)
	num_complaints = df["complaint_type"].value_counts()
	to_remove = num_complaints[num_complaints <= 30].index
	df.replace(to_remove, np.nan, inplace=True)
	return df


def connect_sql_server():
	# Formatted connection string for the SQL DB.
	SQL_CONN_STR = "DSN={0};Database={1};UID={2};PWD={3};".format(DB_URL, DB_BATABASE, DB_USR, DB_PWD)
	
	conn = pyodbc.connect(SQL_CONN_STR)
	return conn


def get_monnit_data(sensor_name):
	data = []

	conn = connect_sql_server()
	cursor = conn.cursor()
	SQL = '''
		SELECT TOP (1000) s.sensorName
			,r.[messageDate]
			,r.[rawData]
			,r.[dataValue]
			,dt.[dataType]
			,r.[plotValue]
			,pl.[plotLabel]
		FROM [salfordMove].[dbo].[READINGS] AS r
		JOIN [salfordMOVE].[dbo].SENSORS AS s
			ON (r.sensorID = s.sensorID)
		JOIN [salfordMOVE].[dbo].PLOT_LABELS as pl
			ON (r.plotLabelID = pl.plotLabelID)
		JOIN [salfordMOVE].[dbo].DATA_TYPES as dt
			ON (r.dataTypeID = dt.dataTypeID)
		WHERE s.sensorName = ?
		ORDER BY messageDate DESC
	'''

	params = str(sensor_name)
	cursor.execute(SQL, params)
	rows = cursor.fetchall()
	conn.close()

	for row in rows:
		data.append(list(row))
		labels = ['sensorName', 'messageDate','rawData', 'dataValue', 'dataType', 'plotValue', 'plotLabel']
		df = pd.DataFrame.from_records(data, columns=labels)
	
	return df