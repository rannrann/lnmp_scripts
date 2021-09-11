#!/bin/bash
 mysql -e "select count(*) from wordpress.wp_comments" &> /dev/null
 echo $?