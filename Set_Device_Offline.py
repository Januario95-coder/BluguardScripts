import time
import mysql.connector as mysql
from General_Functions import config



def Set_Device_Offline():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''UPDATE TBL_Device
                SET Device_Status = 'OFFLINE', Device_Bat_Level = %s,
                    Device_Temp = %s, Device_HR = %s, Device_O2 = %s
                WHERE TIMEDIFF(CURRENT_TIMESTAMP(),
                                CONCAT(Device_Last_Updated_Date, ' ',
                                Device_Last_Updated_Time)) > "00:00:10";
    '''
    parameters = (0, 0, 0, 0)
    Cursor.execute(query, parameters)
    Connector.commit()

    query = '''UPDATE TBL_Device
                SET Device_Bat_Level = %s,
                    Device_Temp = %s,
                    Device_HR = %s, Device_O2 = %s
                WHERE Device_Status = %s OR Incorrect_Data_Flag = %s
    '''
    parameters = (0, 0, 0, 0, 'OFFLINE', 1)
    Cursor.execute(query, parameters)
    Connector.commit()
    print('Setting device to offline')

Set_Device_Offline()

# try:
#     while True:
#         Set_Device_Offline()
#         time.sleep(3)
#         print('Setting device to offline')
# except KeyboardInterrupt:
#     print('Operation canceled')
# except Exception:
#     print('Operation stopped')

