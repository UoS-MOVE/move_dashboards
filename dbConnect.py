# Title: Database Connector
# Description: 
# Author: Ethan Bellmer
# Date: 05/02/2020
# Version: 0.1


import pyodbc


# Formatted connection string for the SQL DB.
SQL_CONN_STR = 'DSN=Salford-SQL-Server;'

# Function definitiions for DB functions
def fetchData():
	print('Fetch data function')
	TABLE = 'sensorData'	
def updateData():
	print('Update data function')
	TABLE = 'gatewayData'
def fetchUser():
	print('Fetch user function')
	TABLE = 'moveUsers'


# Execute query on database
#cursor.execute("INSERT INTO " + dbTable + columns + " VALUES (" + str(gatewayID) + ",'" + str(gatewayName) + "'," + str(accountID) + "," + str(networkID) + "," + str(messageType) + "," + str(gatewayPower) + "," + str(batteryLevel) + ",'" + str(gatewayDate) + "'," + str(gatewayCount) + "," + str(signalStrength) + "," + str(pendingChange) + ")")
#cursor.execute("INSERT INTO " + dbTable + columns + " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [gatewayID, str(gatewayName), accountID, messageType, gatewayPower, batteryLevel, datetime.date(gatewayDate), gatewayCount, signalStrength, pendingChange])
