import mysql.connector

#host = 'localhost'
host = 'mytravel.c3wvcztuagdw.us-east-2.rds.amazonaws.com'
#database = 'mytravel'
database ='mytravelnyc'
#user = 'root'
user = 'admin'
#password = ''
password ='camargo13'


conn = mysql.connector.connect(host=host, user=user, password=password,database=database)

cursor = conn.cursor()
