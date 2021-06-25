import os
import json
import time
import logging
import requests
import datetime as dt
from datetime import datetime
import mysql.connector as mysql
from General_Functions import config
from requests import HTTPError, ConnectionError as ReqError



def Save_To_Logging():
    logger = logging.getLogger('Crest Check In Vitals')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('C:/Users/hayysoft/Documents/LogFiles/Crest_Check_In_Vitals.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('\nProgram started!')
    logger.info('Program Finished!\n')

    print('INFO saved to logging file after POST request')




def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def Crest_Check_In_Vitals():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT * FROM TBL_Crest_Patient
        WHERE Patient_Discharged = %s
    '''
    parameter = (0,)
    Cursor.execute(query, parameter)
    patients = dictfetchall(Cursor)

    for patient_row in patients:
        Device_Tag = patient_row['Device_Tag']
        print(f'Device_Tag = {Device_Tag}')
        Patient_Tag = patient_row['Patient_Tag']
        print(f'Patient_Tag = {Patient_Tag}')
        Patient_ID = patient_row['Patient_ID']
        print(f'Patient_ID = {Patient_ID}')
        query = '''
            SELECT CONCAT(Device_Last_Updated_Date, " ",
                          Device_Last_Updated_Time) AS datetime,
                    Device_Temp AS temperature, Device_HR AS heartrate,
                    Device_O2 AS SpO2, Device_ID,
                    Gateway_Mac, Device_Tag
            FROM TBL_Device
            WHERE Device_Tag = %s
        '''
        parameters = (Device_Tag,)
        Cursor.execute(query, parameters)
        results = dictfetchall(Cursor)

        try:
            row = results[0]
            query = '''
                SELECT Gateway_Latitude AS latitude,
                       Gateway_Longitude AS longitude
                FROM TBL_Gateway
                WHERE Gateway_Mac = %s
            '''
            Gateway_Mac = row['Gateway_Mac']
            parameter = (Gateway_Mac,)
            Cursor.execute(query, parameter)
            Lat_Lng = dictfetchall(Cursor)
            try:
                row.update(Lat_Lng[0])
            except LookupError:
                row.update({
                    'latitude': 999.99,
                    'longitude': 999.99
                })

            row.update({
                'subject_id': Patient_Tag
            })

            row['checkin'] = 1
            row['temperature_finger'] = 999.99
            row['SpO2_finger'] = 999
            row['heartrate_finger'] = 999
            row['respiratory_rate'] = 999

            del row['Gateway_Mac']
            del row['Device_ID']
            row_ = {
                "subject_id": row['subject_id'],
                "device_id": row['Device_Tag'],
                "datetime": row['datetime'],
                "latitude": row['latitude'],
                "longitude": row['longitude'],
                "checkin": row['checkin'],
                "temperature": row['temperature'],
                "SpO2": row['SpO2'],
                "heartrate": row['heartrate'],
                "temperature_finger": row['temperature_finger'],
                "SpO2_finger": row['SpO2_finger'],
                "heartrate_finger": row['heartrate_finger'],
                "respiratory_rate": row['respiratory_rate'],
            }

            # Convert datetime to UNIX
            datetime_val = datetime.strptime(row_['datetime'], '%Y-%m-%d %H:%M:%S')
            datetime_val = int(datetime_val.timestamp())
            print(datetime.utcfromtimestamp(datetime_val).strftime('%Y-%m-%d %H:%M:%S'))

            # Set datetime to the converted UNIX timestamp
            row_['datetime'] = datetime_val

            print(json.dumps(row_, indent=4))

            # Make a post request to checkin_vital Crest API
            url = 'http://dhri.crc.gov.my/patient/checkin_vital'
            response = requests.post(url, data=json.dumps(row_), headers={
                'Authorization': 'Token 7c1899d4eab19ad83c585390c84586f3e385610c',
                'Content-Type': 'application/json'
            })
            print(f'Status:{response.status_code}')
            # print(f'Response: {response.json()}')
            print(f'Reason: {response.reason}')

            # After successfull POST request
            # UPDATED Last_Vitals_Datetime inside tbl_patient
            if response.status_code == 200:
                query = '''
                    UPDATE TBL_Crest_Patient
                    SET Last_Vitals_Datetime = CURRENT_TIMESTAMP()
                    WHERE Patient_ID = %s
                '''
                parameter = (Patient_ID,)
                Cursor.execute(query, parameter)
                Connector.commit()

                Save_To_Logging()
        except LookupError:
            pass



Crest_Check_In_Vitals()

print('Crest_Check_In_Vitals.py ran successfull!')
time.sleep(3)



