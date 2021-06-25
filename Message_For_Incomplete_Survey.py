import time
import datetime as dt
from datetime import datetime, timedelta
import mysql.connector as mysql
from General_Functions import config



def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def checking_Time(hour):
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    date = dt.datetime(year, month, day, hour, 0, 0, 0)
    return date



def Update_TBL_Message(Message_Description, Message_Date,
                       Message_Time, Message_Type, Wearer_ID):
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        INSERT INTO TBL_Message
            (Message_ID, Message_Description, Message_Date,
             Message_Time, Message_Type, Wearer_ID)
        VALUES ((SELECT Create_PK("MSG")), %s, %s, %s, %s, %s)
    '''

    parameters = (Message_Description, Message_Date,
                  Message_Time, Message_Type, Wearer_ID)
    Cursor.execute(query, parameters)
    Connector.commit()
    print('Saved successfully!')



def Message_For_Incomplete_Survey():
    Connector = mysql.connect(**config)
    Cursor = Connector.cursor()

    query = '''
        SELECT Patient_ID, Last_Survey_Datetime, Wearer_ID FROM TBL_Crest_Patient
        WHERE Patient_Discharged = %s
    '''
    parameter = (0,)
    Cursor.execute(query, parameter)
    results = dictfetchall(Cursor)
    for row in results:
        Last_Survey_Datetime = row['Last_Survey_Datetime']
        Wearer_ID = row['Wearer_ID']
        Message_Description = 'Please, complete the overdue survey'
        today = datetime.today()
        Message_Date = today.date()
        Message_Time = today.time()
        Message_Type = 'Info'

        try:
            if (datetime.now() > checking_Time(9) and
                datetime.now() < checking_Time(16)):
                if (Last_Survey_Datetime > checking_Time(9) and
                    Last_Survey_Datetime < checking_Time(16)):
                    pass
                else:
                    Update_TBL_Message(Message_Description, Message_Date,
                                       Message_Time, Message_Type, Wearer_ID)
            elif (datetime.now() > checking_Time(16) and
                  datetime.now() < checking_Time(9) + timedelta(hours=24)):
                if (Last_Survey_Datetime > checking_Time(16) and
                    Last_Survey_Datetime < checking_Time(9) + timedelta(hours=24)):
                    pass
                else:
                    Update_TBL_Message(Message_Description, Message_Date,
                                       Message_Time, Message_Type, Wearer_ID)
        except TypeError:
            pass


Message_For_Incomplete_Survey()

print('Message_For_Incomplete_Survey.py ran successfull!')
time.sleep(3)
