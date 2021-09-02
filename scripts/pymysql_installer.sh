#!/bin/bash
rm -rf /root/.pip
mkdir /root/.pip
echo "[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple/" > /root/.pip/pip.conf
pip3 install pymysql &> /dev/null
