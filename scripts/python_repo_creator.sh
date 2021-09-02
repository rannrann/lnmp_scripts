#!/bin/bash
echo "[Python]
name=python3
baseurl=ftp://192.168.2.254/python-packages
enabled=1
gpgcheck=0" > /etc/yum.repos.d/python.repo
yum clean all &> /dev/null
yum repolist &> /dev/null
yum -y install python3 &> /dev/null
