#!/bin/bash
echo "$1:6789:/ /usr/local/nginx/html/ ceph defaults,_netdev,name=admin,secret=$2 0 0" >> /etc/fstab