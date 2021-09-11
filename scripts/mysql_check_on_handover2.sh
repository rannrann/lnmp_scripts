#!/bin/bash
 mysql -uwordpress -pwordpress -h$1 -e "select count(*) from wordpress.wp_comments" &> /dev/null
 echo $?