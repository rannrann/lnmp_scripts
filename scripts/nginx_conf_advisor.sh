#!/bin/bash
sed -i '45s/index.html/index.php index.html/' /usr/local/nginx/conf/nginx.conf
sed -i '65,71s/#//' /usr/local/nginx/conf/nginx.conf
sed -i '/scripts$fastcgi_script_name/s/fastcgi_param/#fastcgi_param/' /usr/local/nginx/conf/nginx.conf
sed -i '/fastcgi_params;/s/fastcgi_params/fastcgi.conf/' /usr/local/nginx/conf/nginx.conf
echo "test php" > /usr/local/nginx/html/test.php
systemctl start nginx php-fpm &> /dev/null