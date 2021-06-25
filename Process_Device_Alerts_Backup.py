import os
import json
import time
import logging
import datetime as dt
from datetime import datetime
import mysql.connector as mysql
from General_Functions import Create_PK


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def Insert_Alert(Alert_Code, Alert_Reading, device_id):
    query = '''
        INSERT INTO TBL_Alert
            (Alert_ID, Alert_Code, Alert_Reading,
             Alert_Date, Alert_Time, Device_ID)
            VALUES(%s, %s, %s, CURDATE(), CURTIME(), %s)
    '''
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    parameters = (Create_PK('ALT'), Alert_Code, Alert_Reading, device_id)
    Cursor.execute(query, parameters)
    Connector.commit()


def Check_Highest_Score(Type, low_attr, high_attr, attr_value, device_id):
    if Type == 'temp':
        if high_attr == 5:
            Insert_Alert(1, attr_value, device_id)
            print('Insert Alert_Code 1')
        elif low_attr == 5:
            Insert_Alert(2, attr_value, device_id)
            print('Insert Alert_Code 2')
    elif Type == 'heart_rate':
        if high_attr == 5:
            Insert_Alert(3, attr_value, device_id)
            print('Insert Alert_Code 3')
        elif low_attr == 5:
            Insert_Alert(4, attr_value, device_id)
            print('Insert Alert_Code 4')
    elif Type == 'spo2':
        if high_attr == 5:
            Insert_Alert(5, attr_value, device_id)
            print('Insert Alert_Code 5')
        elif low_attr == 5:
            Insert_Alert(6, attr_value, device_id)
            print('Insert Alert_Code 6')
    elif Type == 'batlevel':
        if low_attr == 5:
            Insert_Alert(7, attr_value, device_id)
            print('Insert Alert_Code 7')


def Process_Score(Type, low_attr, high_attr, attr_value):
    if Type == 'temp':
        if attr_value < 35:
            low_attr += 1
        elif attr_value > 37:
            high_attr += 1
    elif Type == 'heart_rate':
        if attr_value < 60:
            low_attr += 1
        elif attr_value > 100:
            high_attr += 1
    elif Type == 'spo2':
        if attr_value < 95:
            low_attr += 1
        elif attr_value > 100:
            high_attr += 1
    elif Type == 'batlevel':
        if attr_value < 50:
            low_attr += 1
        elif attr_value > 100:
            high_attr += 1

    return (low_attr, high_attr, attr_value)



LtempScore, HtempScore, LastTemp = 0, 0, 0
LhrScore, HhrScore, LastHR = 0, 0, 0
LO2Score, HO2Score, LastO2 = 0, 0, 0
LHRScore, HHRScore, LastHR = 0, 0, 0

def Process_Individual_File(filename):
    global LtempScore, HtempScore, LastTemp
    global LhrScore, HhrScore, LastHR
    global LO2Score, HO2Score, LastO2
    global LHRScore, HHRScore, LastHR

    LtempScore, HtempScore, LastTemp = 0, 0, 0
    LhrScore, HhrScore, LastHR = 0, 0, 0
    LO2Score, HO2Score, LastO2 = 0, 0, 0
    LHRScore, HHRScore, LastHR = 0, 0, 0

    with open(filename) as fp:
        data = json.loads(fp.read())

    for row in data[len(data)-5:]:
        print(row)
        LtempScore, HtempScore, LastTemp = Process_Score('temp', LtempScore,
                                                         HtempScore, row['temp'])
        LhrScore, HhrScore, LastHR = Process_Score('heart_rate', LhrScore,
                                                   HhrScore, row['heart_rate'])
        LO2Score, HO2Score, LastO2 = Process_Score('spo2', LO2Score,
                                                  HO2Score, row['spo2'])
        LHRScore, HHRScore, LastHR = Process_Score('batlevel', LHRScore,
                                                  HHRScore, row['batlevel'])

    print(f'LtempScore = {LtempScore}, HtempScore = {HtempScore}')
    print(f'LastTemp = {LastTemp}')
    print(f'LhrScore = {LhrScore}, HhrScore = {HhrScore}')
    print(f'LastHR = {LastHR}')
    print(f'LO2Score = {LO2Score}, HO2Score = {HO2Score}')
    print(f'LastO2 = {LastO2}')
    print(f'LHRScore = {LHRScore}, HHRScore = {HHRScore}')
    print(f'LastHR = {LastHR}')

    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    device_mac = filename.split('.')[0]
    query = '''
        SELECT Device_ID FROM TBL_Device
        WHERE Device_Mac = %s
    '''
    parameter = (device_mac,)
    Cursor.execute(query, parameter)
    results = dictfetchall(Cursor)
    Device_ID = results[0]['Device_ID']

    Check_Highest_Score('temp', LtempScore, HtempScore, LastTemp, Device_ID)
    Check_Highest_Score('heart_rate', LhrScore, HhrScore, LastHR, Device_ID)
    Check_Highest_Score('spo2', LO2Score, HO2Score, LastO2, Device_ID)
    Check_Highest_Score('batlevel', LHRScore, HHRScore, LastHR, Device_ID)


os.chdir('C:/Users/hayysoft/Documents/Scripts/interview/media')
from glob import glob
files = glob("*.json")
files = [file for file in files if len(file) == len(file) == 17]


# for file in files:
#     Process_Individual_File(file)


try:
    logger = logging.getLogger('Process_Device_Alerts')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('C:/Users/hayysoft/Documents/LogFiles/Process_Device_Alerts.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('\nProgram started!')

    for file in files:
        Process_Individual_File(file)
except KeyboardInterrupt as e:
    logger.exception(e)
except Exception as e:
    logger.exception(e)
finally:
    logger.info('Program Finished!\n')



print('Process_Device_Alerts.py ran successfully!')
time.sleep(3)
