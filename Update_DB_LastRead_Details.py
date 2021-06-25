import mysql.connector as mysql
from datetime import datetime
import json



class MySQLConnector:

	def __init__(self, db_name):
		try:
			self.connector = mysql.connect(
				user='root',
				password='Hayysoft',
				host='localhost',
				port=3306,
				database=db_name
			)
		except Exception as e:
			print(e.msg)

	def add_new_data(self, data):
		data_to_insert =[]
		for row in data:
			if row:
				timestamp = row['timestamp'].split('T')
				# if row['band_mac'] == 'CFE2BBA5F086':
				# 	time = datetime.now().time()
				# else:
				# 	time = timestamp[1].split('.')[0]
				
				# date = timestamp[0]
				# time = datetime.now().time()
				# row['date'] = date
				# row['time'] = time
				# row['type'] = 'Unknown'
				# del row['timestamp']
				row = self.format_data(row)
				values = tuple(row.values()) 
				data_to_insert.append(values)

		cursor = self.connector.cursor()
		cursor.executemany('''INSERT INTO TBL_Incoming
			(Incoming_Device_Mac, Incoming_Gateway_Mac, Incoming_Temp, Incoming_O2, Incoming_HR, Incoming_Date, Incoming_Time)
			VALUES (%s, %s, %s, %s, %s, %s, %s)''', data_to_insert)
		self.connector.commit()
		self.connector.close()
		print('Data inserted successfully!')

	def format_data(self, data):
		data = {
			'Incoming_Device_Mac': data['device_mac'],
			'Incoming_Gateway_mac': data['gateway_mac'],
			'Incoming_Temp': data['temp'],
			'Incoming_O2': data['spo2'],
			'Incoming_HR': data['heart_rate'],
			'Incoming_Date': data['date'],
			'Incoming_Time': data['time']	
		}

		return data


# with open('D:/Scripts/interview/media/raw_data.json') as fp:
# 		data = json.loads(fp.read())

# connector = MySQLConnector('bluguarddb')
# connector.add_new_data(data)
