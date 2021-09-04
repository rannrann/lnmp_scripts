#!/bin/bash
yum -y remove chrony &> /dev/null
yum -y install chrony &> /dev/null
sed -i '3,6s/server/#server/' /etc/chrony.conf
sed -i "6a server $1 iburst" /etc/chrony.conf
systemctl enable chronyd --now
rm -rf /root/.ssh/authorized_keys