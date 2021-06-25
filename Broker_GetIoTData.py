#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 17:48:43
"""

import string
import json
import datetime
from Process_IoTData import Get_Mqtt_Data



def Read_Gateway_Data(raw_data):
	"""Accepts raw data from the gateway and decodes to
	utf-8, then replaces single quotes with double quotes.

	Create a json data from the raw data.
	Call Get_Mqtt_Data function with the raw data.
	"""
	mqtt_data = raw_data.decode('utf-8').replace("'", '"')
	mqtt_data = json.loads(mqtt_data)
	print('\n----- Data Begin ----->')
	Get_Mqtt_Data(mqtt_data)
	print('----- Data End ----->\n')


def Message(client, obj, msg):
	"""Load raw data from gateway in the msg parameter.
	Call Read_Gateway_Data with the raw data
	from the gateway."""
	Read_Gateway_Data(msg.payload)










