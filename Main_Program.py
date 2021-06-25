#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 18:31:43
"""


from Broker_Connect import Client
from Broker_GetIoTData import Message


client_instance = Client()  # Instantiate mqtt client
client_instance.client_.on_message = Message  # Set on_message function to receive
									          # data from gateway
client_instance.Start_connection()  # Initiate connection




