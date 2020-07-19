import mysql.connector


host = 'amazonaws.com'

database =''

user = ''
password = ''



conn = mysql.connector.connect(host=host, user=user, password=password,database=database)

cursor = conn.cursor()
