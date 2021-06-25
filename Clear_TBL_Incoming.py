
import mysql.connector as mysql


def Clear_TBL_Incoming():
	Connector = mysql.connect(
		user='root',
		password='Hayysoft',
		host='localhost',
		port=3306,
		database='bluguarddb'
	)

	Cursor = Connector.cursor()
	Cursor.execute('TRUNCATE TABLE TBL_Incoming;')

	Connector.commit()
	Connector.close()


Clear_TBL_Incoming()