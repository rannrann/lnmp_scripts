#!/bin/python3
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    charset='utf8'
)
cursor = conn.cursor()
sql = "select count(*) from information_schema.SCHEMATA where SCHEMA_NAME = 'wordpress';"
cursor.execute(sql)
if_db_exists = cursor.fetchone()

sql = "select count(*) from mysql.user where User='wordpress';"
cursor.execute(sql)
user_amount = cursor.fetchone()


cursor.close()
conn.close()

if if_db_exists[0] == 1 and user_amount[0] == 2:
    print('True')
else:
    print('False')