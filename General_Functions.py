import datetime
import mysql.connector as mysql


config = {
    'host': 'bgplatformdb1.mysql.database.azure.com',
    'user': 'bg37hayysoftadmin',
    'password': 'DoNotHack2021',
    'database': 'bluguarddb',
    # 'client_flags': [mysql.ClientFlag.SSL],
    # 'ssl_ca': 'C',
    'port': '3306'
}



def Create_PK(ID):
    """Creates a primary_key for a given table
    with ID parameter specifying the initials of the table name

    parameter
    ---------
        Create_PK("IN")
            >> IN2021-06-10T12:53:45.513819
    """
    return ID + 'T'.join(str(datetime.datetime.now()).split(' '))



def Validate_Raw_Data_Length(device_type, raw_data_length):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Raw_Data_Length FROM TBL_Device_Raw_Length
        WHERE Device_Type = %s AND Raw_Data_Length = %s
    '''
    parameters = (device_type, len(raw_data_length))
    Cursor.execute(query, parameters)
    results = Cursor.fetchall()

    return True if len(results) != 0 else False


