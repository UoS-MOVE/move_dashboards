# Title: Database Connector
# Description: 
# Author: Ethan Bellmer
# Date: 05/02/2020
# Version: 0.1


import pyodbc


# Formatted connection string for the SQL DB.
SQL_CONN_STR = 'DSN=Salford-SQL-Server;'

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
	cursor.execute("SELECT DISTINCT sensorName FROM ?", dbTable)
	result = cursor.fetchall()
	conn.close()
	return result
def fetchData(dbTable, dbColumn, dbColumnValue, startDate, endDate):
	print('Fetching senor data... ')
	TABLE = dbTable
	COLUMN = dbColumn
	COLUMN_VALUE = dbColumnValue
	START_DATE = startDate
	END_DATE = endDate

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

	# Select all available data from a specified table using specified parameters to filter the data
	cursor.execute("SELECT plotValues, messageDate FROM ? WHERE ? = ? AND messageDate < ? AND messageDate > ?", TABLE, COLUMN, COLUMN_VALUE, START_DATE, END_DATE)
	result = cursor.fetchall()
	conn.close()
	return result

def updateData():
	print('Updating data... (currently unused)')
	TABLE = 'gatewayData'

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

def fetchUsername(uName):
	print('Fetching username... ')
	TABLE = 'moveUsers'
	USER = uName

	# Establish a connection to the database using the prepared function and declare a new cursor from it
	conn = dbInit()
	cursor = conn.cursor()

	# Select a specified username from the user table and return the result, used for checking the existence of a user 
	cursor.execute("SELECT user FROM ? WHERE user = ?", TABLE, USER).rowcount
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
	cursor.execute("SELECT user, password, salt FROM ? WHERE user = ?", TABLE, USER)
	usrCreds = cursor.fetchall()
	# Close the open database connetion
	conn.close()
	# Return the retrieved values
	return usrCreds
