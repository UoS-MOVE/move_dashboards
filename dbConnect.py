# Title: Database Connector
# Description: 
# Author: Ethan Bellmer
# Date: 05/02/2020
# Version: 0.1


import pyodbc
import json

import pandas as pd

#SQL Server connection info
with open(".dbCreds") as f:
	dbCreds = json.load(f)


# Formatted connection string for the SQL DB.
SQL_CONN_STR = 'DSN=Salford-SQL-Server;Database=salfordMOVE;Trusted_Connection=no;UID='+dbCreds['UNAME']+';PWD='+dbCreds['PWD']+';'

# Function definitiions for DB functions
def dbInit():
	try:
		print('Connecting to database...')
		# Create a new connection to the SQL Server using the prepared connection string
		cnxn = pyodbc.connect(SQL_CONN_STR)
	except pyodbc.Error as e:
		# Print error is one should occur
		sqlstate = e.args[1]
		print("An error occurred connecting to the database: " + sqlstate)
		#abort(500)
		return 500
	else:
		print('Successfully connected to database')
		return cnxn
def fetchSensorNames(dbTable):
	print('Fetching sensor names... ')

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()
	
	# Select all available data from a specified table using specified parameters to filter the data
	
	result = pd.read_sql("SELECT DISTINCT sensorName FROM " + dbTable + "", conn)	
	print('Sensor names successfully fetched')

	conn.close()
	return result

def fetchData(dbTable):
	print('Fetching senor data... ')

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

	# Select all available data from a specified table using specified parameters to filter the data	
	#result = pd.read_sql("SELECT sensorName, plotValues, messageDate FROM " + dbTable + " WHERE messageDate < ? AND messageDate > ?", conn, params={ startDate, endDate})
	result = pd.read_sql("SELECT sensorName, plotValues, messageDate FROM " + dbTable + "", conn)
	print('Sensor data successfully fetched')

	#result = cursor.fetchall()
	conn.close()
	return result



	#df = pd.read_sql(('select "Timestamp","Value" from "MyTable" '
	#	'where "Timestamp" BETWEEN %(dstart)s AND %(dfinish)s'),
	#db,params={"dstart":datetime(2014,6,24,16,0),"dfinish":datetime(2014,6,24,17,0)},
	#index_col=['Timestamp'])


def updateData():
	print('Updating data... (currently unused)')
	TABLE = 'gatewayData'

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

def fetchUsername(uName):
	print('Fetching username... (currently unused)')
	TABLE = 'moveUsers'
	USER = uName

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

	# Select a specified username from the user table and return the result, used for checking the existence of a user 
	cursor.execute("SELECT user FROM " + TABLE + " WHERE user = ?", USER).rowcount
	usrCount = cursor.fetchall()
	conn.close()
	return usrCount
def fetchUserPWD(uName):
	print('Fetching user credentials... ')
	TABLE = 'moveUsers'
	USER = uName

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

	# Select the specified user's credentials such as hashed password and salt for authorisation
	cursor.execute("SELECT user, password, salt FROM " + TABLE + " WHERE user = ?", USER)
	usrCreds = cursor.fetchall()
	# Close the open database connetion
	conn.close()
	# Return the retrieved values
	return usrCreds
