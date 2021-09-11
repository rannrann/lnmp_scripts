#!/bin/bash
mysql -e 'select count(*) from mysql.user where User="wordpress"'