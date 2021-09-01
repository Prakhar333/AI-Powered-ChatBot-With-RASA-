import mysql.connector
from datetime import datetime

from mysql.connector import optionfiles

def dataUpdate(name,phone,time,section):
    mydb = mysql.connector.connect(
            option_files = 'my.conf'
        )
    mycursor = mydb.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    query = 'INSERT INTO persons (name,phone,time,Section,Time_of_booking) VALUES("{0}","{1}","{2}","{3}","{4}");'.format(name,phone,time,section,formatted_date)
    mycursor.execute(query)
    mydb.commit()
        #mydb.commit()
        #res = mycursor.fetchall()