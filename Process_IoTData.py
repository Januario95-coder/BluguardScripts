#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 18:31:43
"""

import json
from datetime import datetime
from read_json import ManageJson
import mysql.connector as mysql
from General_Functions import (
	Create_PK, Validate_Raw_Data_Length
)




config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}


def Extract_MetaData(data, key):
	"""Returns the value for the given inside
	data dictionary."""
	return data.get(key)


def Start_Process_IoTData(data_from_gateway):
	pass


def Convert_Hex_To_Decimal(hex_data):
	"""Converts hexadecimal data to decimal.
	Returns decimal data"""
	try:
		decimal_data = int(hex_data, 16)
		return decimal_data
	except (ValueError, TypeError):
		return ''

def Get_Vital_Temp(raw_data,
				   temp_startpos,
				   temp_endpos):
	"""Extracts temperature in hexadecimal and
	returns the temperature in decimal from the rawdata.

	Parameters
	-----------------
	raw_data:		 the raw data to be extracted from
	temp_startpos:	 is the starting position of the temperature
					 in raw data.
	temp_endpos:	 is the ending position (not inclusive) of the
					 temperature in raw data.

	Returns
	------
	temperature:     temperature converted to decimal from hexadecimal

	Exmple:
		>> Get_Vital_Temp('0EFF3412CFE2BBA5F0860301420016',
						20, 24)
	"""
	temp_ = raw_data[temp_startpos:temp_endpos]
	temp_ = temp_[2:4] + temp_[0:2]
	print(f'| raw_temp = {temp_}')
	temperature = Convert_Hex_To_Decimal(temp_) / 10
	return temperature

def Get_Vital_Heart_Rate(raw_data,
						 heart_rate_startpos,
						 heart_rate_endpos):
	"""Extracts and returns the heartrate from the rawdata.

	Implementation of this function follows the same
	logic as the Get_Vital_Temp function above.
	"""
	heart_rate_ = raw_data[heart_rate_startpos:heart_rate_endpos]
	print(f'| raw_heart_rate = {heart_rate_}')
	return Convert_Hex_To_Decimal(heart_rate_)

def Get_Vital_Spo2(raw_data,
				   spo2_startpos,
				   spo2_endpost):
	"""Extracts and returns the spo2 from the rawdata.

	Implementation of this function follows the same
	logic as the Get_Vital_Temp function above.
	"""
	spo2 = raw_data[spo2_startpos:spo2_endpost]
	print(f'| raw_spo2 = {spo2}')
	return Convert_Hex_To_Decimal(spo2)

def Get_Status_Batlevel(raw_data,
				 		batlevel_startpos,
				 		batlevel_endpost):
	"""Extracts and returns the spo2 from the rawdata.

	Implementation of this function follows the same
	logic as the Get_Vital_Temp function above.
	"""
	batlevel = raw_data[batlevel_startpos:batlevel_endpost]
	print(f'| raw_batlevel = {batlevel}')
	return Convert_Hex_To_Decimal(batlevel)


def Get_Device_Type(Device_Mac):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	query = '''
		SELECT Device_Type FROM tbl_device
		WHERE Device_Mac = %s
	'''
	parameter = (Device_Mac,)
	Cursor.execute(query, parameter)
	results = Cursor.fetchall()
	try:
		results = results[0][0]
	except IndexError:
		results = []
	return results


def HSWB001_Process_Data(raw_data):
	temperature = raw_data[16:18] + raw_data[14:16]
	temperature = int(temperature, 16) / 10
	heart_rate = Get_Vital_Heart_Rate(raw_data, 22, 24)
	spo2 = Get_Vital_Spo2(raw_data, 24, 26)
	batlevel = Get_Status_Batlevel(raw_data, 26, 28)
	vital_data = {
		'temp': temperature,
		'heart_rate': heart_rate,
		'spo2': spo2,
		'batlevel': batlevel
	}
	return vital_data


def Process_RawData(raw_data, device_type):
	"""Extracts temperature, heart_rate, spo2, batlevel
	from raw data based on the device type
	"""
	if device_type == 'HSWB001':
		data = HSWB001_Process_Data(raw_data)
		return data
	elif device_type == 'HSWB002' and len(raw_data) == 56:
		try:
			temperature = raw_data[40:42] + raw_data[38:40]
			temperature = int(temperature, 16) / 100
			heart_rate = Get_Vital_Heart_Rate(raw_data, 52, 54)
		except ValueError:
			pass

		data = {
			'temp': temperature,
			'heart_rate': heart_rate,
			'spo2': 0,
			'batlevel': 0
		}
		return data


def Extract_Device_Mac(data):
	device_macs = []
	for key, value in data.items():
		if key == 'mac':
			if data.get('type') != 'Gateway':
				device_macs.append(value)

	return device_macs


def Populate_MetaData(data, gateway_mac):
	Metadata_ = {}
	Metadata_['timestamp'] = data['timestamp']
	timestamp = data[ 'timestamp'].split('T')
	date = timestamp[0]
	time = datetime.now().time()
	Metadata_['date']  = f'{date}'
	Metadata_['time'] = f'{time}'
	Metadata_['gateway_mac'] = gateway_mac
	Metadata_['device_mac'] = data['mac']
	Metadata_['bleName'] = data["bleName"]
	Metadata_['rssi'] = data['rssi']

	return Metadata_


def Process_Quarentine_Band(data, gateway_mac, Device_Mac, Device_Type):
	Connector = mysql.connect(**config)

	Cursor = Connector.cursor()

	populate_metadata = Populate_MetaData(data, gateway_mac)
	# print(populate_metadata)

	query_to_tbl_device = '''
		UPDATE TBL_Device
			SET Device_Last_Updated_Date = %s,
				Device_Last_Updated_Time = %s,
	            Device_Temp = %s,
	            Device_HR = %s,
	            Device_O2 = %s,
	            Incorrect_Data_Flag = %s,
	            Incorrect_Data_Flag = %s,
	            Device_Status = "ONLINE"
	        WHERE Device_Mac = %s
	'''
	parameters_to_tbl_device = (populate_metadata['date'],
			  	  				populate_metadata['time'], 0, 0, 0, 0, 0, Device_Mac)
	Cursor.execute(query_to_tbl_device, parameters_to_tbl_device)
	Connector.commit()



def Filter_Message(validated, Device_Type, Raw_Data, data, gateway_mac, Device_Mac):
	populate_metadata = Populate_MetaData(data, gateway_mac)

	Connector = mysql.connect(**config)
	Cursor = Connector.cursor()

	query_to_tbl_device = '''
		UPDATE TBL_Device
			SET Device_Last_Updated_Date = %s,
				Device_Last_Updated_Time = %s,
	            Device_Temp = %s,
	            Device_HR = %s,
	            Device_O2 = %s,
	            Device_Bat_Level = %s,
	            Incorrect_Data_Flag = %s,
	            Device_Status = "ONLINE"
	        WHERE Device_Mac = %s
	'''

	if validated == False:
		json_manager = ManageJson('incorrect_raw_data')
		data_from_json = json_manager.load_json()
		populate_metadata.update({
			'rawData': Raw_Data
		})
		data_from_json.append(populate_metadata)
		json_manager.save_json(data_from_json)
		print('*' * 10, 'INCORRECT_DATA', '*' * 10)
		print(f'validated = {validated}')
		print(f'rawData = {data["rawData"]}')
		print(f'Device_Mac = {Device_Mac}')
		print(f'device_type = {Device_Type}')

		parameters_to_tbl_device = (populate_metadata['date'],
				  	  				populate_metadata['time'], 0, 0, 0, 0, 1, Device_Mac)
	elif validated == True:
		# Data is correct
		populate_vitaldata = Process_RawData(Raw_Data, Device_Type)
		populate_vitaldata.update(populate_metadata)
		json_manager = ManageJson()
		data_from_json = json_manager.load_json()
		data_from_json.append(populate_vitaldata)
		json_manager.save_json(data_from_json)
		print('*' * 10, 'CORRECT_DATA', '*' * 10)
		print(f'validated = {validated}')
		print(f'rawData = {data["rawData"]}')
		print(f'Device_Mac = {Device_Mac}')
		print(f'device_type = {Device_Type}')
		print(f'batlevel = {populate_vitaldata["batlevel"]}')

		parameters_to_tbl_device = (populate_metadata['date'], populate_metadata['time'],
					  				populate_vitaldata['temp'], populate_vitaldata['heart_rate'],
					  				populate_vitaldata['spo2'], populate_vitaldata['batlevel'], 0,
					  				Device_Mac)

	Cursor.execute(query_to_tbl_device, parameters_to_tbl_device)
	Connector.commit()

	print('Filter_Message function executed successfully!')



def Get_Mqtt_Data(data_from_gateway):
	for data in data_from_gateway:
		print(data)
		if data['type'] == 'Gateway':
			gateway_mac = data['mac']

		if data['type'] != 'Gateway':
			Device_Mac = data['mac']
			Device_Type = Get_Device_Type(Device_Mac)

			if Device_Type == 'HSWB004':
				print(f'Device_Type = {Device_Type}')
				Process_Quarentine_Band(data, gateway_mac, Device_Mac, Device_Type)
			elif data.get('rawData') is not None:
				try:
					results = Validate_Raw_Data_Length(Device_Type, data['rawData'])
					Filter_Message(results, Device_Type, data['rawData'], data,
							   	   gateway_mac=gateway_mac, Device_Mac=Device_Mac)
				except Exception:
					pass

	print('\n\n')





