#!/bin/bash
yum -y remove chrony &> /dev/null
yum -y install chrony &> /dev/null
sed -i '/allow 192.168.0.0/s/#//' /etc/chrony.conf
sed -i "/allow 192.168.0.0/s/0/$1/" /etc/chrony.conf
sed -i '/allow 192.168.0.0/s/\/16/\/24/' /etc/chrony.conf
sed -i '/local stratum/s/#//' /etc/chrony.conf
systemctl enable chronyd --now

