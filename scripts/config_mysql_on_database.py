#!/bin/python3
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    charset='utf8'
)

cursor = conn.cursor()
sql = "DROP DATABASE IF EXISTS wordpress;"
cursor.execute(sql)
sql = "create database wordpress character set utf8mb4;"
cursor.execute(sql)

sql = "select count(*) from mysql.user where User='wordpress';"
cursor.execute(sql)
if_user_exists = cursor.fetchone()
if if_user_exists[0] != 0:
    sql = "delete from mysql.user where User = 'wordpress';"
    cursor.execute(sql)


sql = "grant all on wordpress.* to wordpress@'%' identified by 'wordpress';"
cursor.execute(sql)
sql = "flush privileges;"
cursor.execute(sql)


cursor.close()
conn.close()