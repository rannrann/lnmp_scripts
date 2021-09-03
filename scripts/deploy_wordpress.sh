#!/bin/bash
rm -rf /usr/local/nginx/html/*
unzip /root/wordpress* &> /dev/null
cd /root/wordpress*
tar -xf wordpress* &> /dev/null
cp -r wordpress/* /usr/local/nginx/html/
chown -R apache.apache /usr/local/nginx/html/