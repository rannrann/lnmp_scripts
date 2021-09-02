#!/bin/bash
rm -rf /etc/yum.repos.d/*
echo '[local_repo]
name=CentOS-$releasever - Base
baseurl=ftp://192.168.2.254/centos-1804
enabled=1
gpgcheck=0' > /etc/yum.repos.d/local.repo

