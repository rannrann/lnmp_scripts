#!/bin/bash
mysql -e 'DROP DATABASE IF EXISTS wordpress;'
mysql -e 'create database wordpress character set utf8mb4;'
mysql -e 'delete from mysql.user where User = "wordpress"'
mysql -e "grant all on wordpress.* to wordpress@'localhost' identified by 'wordpress'"
mysql -e "grant all on wordpress.* to wordpress@"$1" identified by 'wordpress'"
mysql -e "flush privileges"