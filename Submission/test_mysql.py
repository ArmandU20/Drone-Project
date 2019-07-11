import MySQLdb
import sys
import datetime
# ------------------------------- MySQL credentials -----------------------------------------
server = 'sql2.freemysqlhosting.net'
username = 'sql2286265'
pswd = 'tE6*aN5%'
database = 'sql2286265'

my_time = datetime.datetime.now()
my_time = str(my_time.strftime("%H:%M:%S"))

val1 = str(25.67)
val2 = str(50)
val3 = str(100)
# -------------------------------------------------------------------------------------------
try:
    db = MySQLdb.connect(server, username, pswd, database)
except:
    "print Failed to connect to database. Exiting"
    sys.exit(1)
finally:
    cursor = db.cursor()

query = "INSERT INTO drone_data (Timestamp, Proximity, Humidity, Temperature) VALUES (%s, %s, %s, %s)"
val = [(my_time, val1+' cm', val2+' %', val3+' Celsius')]

cursor.executemany(query, val)
db.commit()

