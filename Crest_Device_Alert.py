import os
import json
import time
import datetime as dt
from datetime import datetime
import requests
import mysql.connector as mysql
from General_Functions import config


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def Crest_Device_Alert():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Patient_Tag, Device_Tag FROM TBL_Crest_Patient
        WHERE Patient_Discharged = %s
    '''
    parameter = (0,)
    Cursor.execute(query, parameter)
    Device_Tags = dictfetchall(Cursor)
    for row in Device_Tags:
        Device_Tag = row['Device_Tag']
        Patient_Tag = row['Patient_Tag']
        query = '''
            SELECT CONCAT(Device_Last_Updated_Date, " ",
                      Device_Last_Updated_Time) AS datetime,
                Device_Temp AS temperature_alert,
                Device_HR AS heartrate_alert,
                Device_O2 AS SpO2_alert, Device_ID,
                Gateway_Mac, Device_Tag, Device_ID
            FROM TBL_Device
            WHERE Device_Tag = %s
        '''
        parameter = (Device_Tag,)
        Cursor.execute(query, parameter)
        Devices = dictfetchall(Cursor)

        for device_row in Devices:
            try:
                Device_ID = device_row['Device_ID']
                print(Device_ID)
                query = '''
                    SELECT Alert_ID, Alert_Code FROM TBL_Alert
                    WHERE Device_ID = %s AND
                          Sent_To_Crest = %s
                '''
                parameters = (Device_ID, 0,)
                Cursor.execute(query, parameters)
                Alerts = dictfetchall(Cursor)

                print(Alerts)
                for alert_row in Alerts:
                    alert_code = int(alert_row['Alert_Code'])
                    Alert_ID = alert_row['Alert_ID']
                    if alert_code == 1:
                        device_row['temperature_alert'] = 2
                        device_row['heartrate_alert'] = 0
                        device_row['SpO2_alert'] = 0
                    elif alert_code == 2:
                        device_row['temperature_alert'] = 1
                        device_row['heartrate_alert'] = 0
                        device_row['SpO2_alert'] = 0
                    elif alert_code == 3:
                        device_row['heartrate_alert'] = 2
                        device_row['temperature_alert'] = 0
                        device_row['SpO2_alert'] = 0
                    elif alert_code == 4:
                        device_row['heartrate_alert'] = 1
                        device_row['temperature_alert'] = 0
                        device_row['SpO2_alert'] = 0
                    elif alert_code == 5:
                        device_row['SpO2_alert'] = 2
                        device_row['temperature_alert'] = 0
                        device_row['heartrate_alert'] = 0
                    elif alert_code == 6:
                        device_row['SpO2_alert'] = 1
                        device_row['temperature_alert'] = 0
                        device_row['heartrate_alert'] = 0
                    device_row.update({
                        'alert_value': 'N/A',
                        'alert_type': alert_code
                    })

                    query = '''
                        SELECT Gateway_Latitude AS latitude,
                               Gateway_Longitude AS longitude
                        FROM TBL_Gateway
                        WHERE Gateway_Mac = %s
                    '''
                    Gateway_Mac = device_row['Gateway_Mac']
                    parameter = (Gateway_Mac,)
                    Cursor.execute(query, parameter)
                    Lat_Lng = dictfetchall(Cursor)
                    try:
                        device_row.update(Lat_Lng[0])
                    except LookupError:
                        device_row.update({
                            'latitude': 999.99,
                            'longitude': 999.99
                        })

                    device_row.update({
                        'subject_id': Patient_Tag
                    })

                    del device_row['Gateway_Mac']
                    del device_row['Device_ID']

                    device_row['device_id'] = device_row['Device_Tag']
                    del device_row['Device_Tag']

                    device_row['respiratory_alert'] = -999

                    datetime_val = datetime.strptime(device_row['datetime'], '%Y-%m-%d %H:%M:%S')
                    datetime_val = int(datetime_val.timestamp())
                    device_row['datetime'] = datetime_val

                    print(json.dumps(device_row, indent=4))
                    url = 'http://dhri.crc.gov.my/patient/device_alert'
                    response = requests.post(url, json=device_row, headers={  # data=json.dumps(device_row)
                        'Authorization': 'Token 7c1899d4eab19ad83c585390c84586f3e385610c',
                        # 'Content-Type': 'application/json'
                    })
                    # print(f'Status:{response.status_code}')
                    print(f'Response: {response.json()}')
                    print(f'Reason: {response.reason}')

                    if response.status_code == 200:
                        print(f'Status: {response.status_code}')
                        query = '''
                            UPDATE TBL_Alert
                            SET Sent_To_Crest = %s AND
                                Alert_ID = %s
                        '''
                        parameters = (1, Alert_ID)
                        Cursor.execute(query, parameters)
                        Connector.commit()

            except (IndexError, KeyError):
                pass


Crest_Device_Alert()


print('Crest_Device_Alert.py ran successfull!')
time.sleep(3)



