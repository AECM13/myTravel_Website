import mysql.connector

host = 'localhost'
database = 'mytravel'
user = 'root'
password = ''

conn = mysql.connector.connect(host=host, user=user, password=password,database=database)

cursor = conn.cursor()
