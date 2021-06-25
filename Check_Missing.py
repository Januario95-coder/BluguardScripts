
import mysql.connector as mysql


def Check_Missing():
	Connnector = mysql.connect(
		user='root',
		password='Hayysoft',
		host='localhost',
		port=3306,
		database='bluguarddb'
	)

	Cursor = Connnector.cursor()

	Cursor.execute('''SELECT Band_Mac, TIMEDIFF(CURTIME(), Last_Updated_Time) 
		FROM TBL_Device WHERE Last_Updated_Date = CURDATE() 
		AND TIMEDIFF(CURTIME(), Last_Updated_Time) > "00:00:15"''')

	TBL_Device_results = Cursor.fetchall()
	for result in TBL_Device_results:
		print(result)

	Cursor.execute('''INSERT INTO TBL_Alert(Alert_Date, Alert_Time, Band_Mac) 
		SELECT Last_Updated_Date, Last_Updated_Time, Band_Mac
		FROM TBL_Device WHERE Last_Updated_Date = CURDATE() 
			AND TIMEDIFF(CURTIME(), Last_Updated_Time) > "00:00:15";''')

	Connnector.commit()
	Connnector.close()


Check_Missing()