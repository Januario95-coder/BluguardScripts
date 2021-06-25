#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 16:23:43
"""

import paho.mqtt.client as mqtt
import json
import Broker_GetIoTData


# Define event callbacks

def Connect(client, user_data, flags, rc):
	"""Prints the connection count of rc."""
	print(f"rc: result count {rc}. connect() called")

def Publish(client, obj, mid):
	"""Displays mid on publish."""
	print(f"mid: {mid} on publish")

def Subscribe(client, obj, mid, granted_qos):
	"""Prints 'on subscribe' indicating a subscription has been made."""
	print(f'Subscribe: {mid} {granted_qos}')

	
class Client:
	def __init__(self):
		"""Create an mqtt client."""
		self.client_ = mqtt.Client()
		self.__rc = 0

	def __set_event_callbacks(self):
		"""Configure event callbacks for the client."""
		self.client_.on_connect = Connect
		self.client_.on_publish = Publish
		self.client_.on_subscribe = Subscribe

	def __connect_with_credentials(self):
		"""Connect to the client with cloud mqqt broker 
		login credentials."""
		self.client_.username_pw_set("xgvutxaa", "9cMIpVoL4Ujj")
		self.client_.connect('spectacular-pharmacist.cloudmqtt.com',1883,3600)

	def __subscribe(self):
		"""Subscribe topic to the client."""
		self.client_.subscribe("BG37T1", 0)

	def __client(self):
		"""Call __set_event_callbacks(),
		__connect_with_credentials(),
		__subscribe()"""
		self.__set_event_callbacks()
		self.__connect_with_credentials()
		self.__subscribe()

	def Start_connection(self):
		"""Call __client().
		Initiate a while loop with the client
		"""
		self.__client()
		while self.__rc == 0:
			self.__rc = self.client_.loop()
		print(f'rc: {self.__rc}')




