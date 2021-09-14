#!/bin/bash
sed -i '/vrrp_gna_interval/a   vrrp_iptables' /etc/keepalived/keepalived.conf
sed -i '37,$d' /etc/keepalived/keepalived.conf
sed -i '31,33d' /etc/keepalived/keepalived.conf
sed -i "/virtual_ipaddress/a $1" /etc/keepalived/keepalived.conf
sed -i "/$1/s/^/      /" /etc/keepalived/keepalived.conf
sed -i "/priority/s/100/50/" /etc/keepalived/keepalived.conf
sed -i "/state/s/MASTER/BACKUP/" /etc/keepalived/keepalived.conf