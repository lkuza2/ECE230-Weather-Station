# Python 3 script
# Script for project
# 	Reads serial data and sends to Wunderground

import serial
import time
import urllib.request

# Create serial communication with Xbee
port = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=3.0)

# Establish variables
NewData = 0
GetUrl = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=KINTERRE25&PASSWORD=brookSrunninG13&dateutc=now&action=updateraw"

while(True):
	# Data acquisition from Xbee through serial
	data = port.readline()

	if data.startswith(b'Temperature'):
		first, second = data.decode('ascii').split('=')
		TempC = float(second.split(' ')[1])
		TempF = TempC*1.8 + 32.0
		NewData += 1

	elif data.startswith(b'Pressure'):
		first, second = data.decode('ascii').split('=')
		Pressure = float(second.split(' ')[1])
#		Pressure = float(data[10:18].decode('ascii'))
		BaromIn = 0.0295*Pressure
		NewData += 1

	elif data.startswith(b'Approximate'):
		first, second = data.decode('ascii').split('=')
		Altitude = float(second.split(' ')[1])
#		Altitude = float(data[19:25].decode('ascii'))
		NewData += 1

	elif data.startswith(b'Humidity'):
		first, second = data.decode('ascii').split('=')
		Humidity = float(second.split(' ')[1])
#		Humidity = float(data[10:16].decode('ascii'))
		NewData += 1

	# HTTP GET request to send weather data
	ThisUrl = GetUrl
	if (NewData >= 4):
		ThisUrl += "&humidity=" + str(Humidity)
		ThisUrl += "&tempf=" + str(TempF)
		ThisUrl += "&baromin=" + str(BaromIn)

		response = urllib.request.urlopen(ThisUrl).read()

		# Print data and request response to log
#		print("Temp:", TempF, "F")
#		print("Humidity:", Humidity, "%")
#		print("Pressure:", BaromIn, "in Hg")
#		print()
#		print("String used for GET request:")
#		print(ThisUrl)
#		print("Result of HTTP GET", response.decode('ascii'))
#		print()

		NewData = 0
