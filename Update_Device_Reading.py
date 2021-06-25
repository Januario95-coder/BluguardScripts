import time
import datetime
import mysql.connector as mysql
from read_json import ManageJson


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}


def Clear_Raw_Data_Json():
    with open('C:/Users/hayysoft/Documents/Scripts/interview/media/raw_data.json', 'w') as fp:
        fp.write('[]')



def Update_Device():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    file_reader = ManageJson()
    data = file_reader.load_json()
    data_to_save = {}
    for row in data:
        data_to_save[row['device_mac']] = row


    for row in data_to_save.items():
        row_data = row[1]
        object_update = ManageJson(row[0])
        object_update_data = object_update.load_json()
        object_update_data.append(row_data)
        object_update.save_json(object_update_data)


Update_Device()
Clear_Raw_Data_Json()
print('raw_data.json cleared successfully!')
time.sleep(3)
