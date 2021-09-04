#!/bin/bash
echo "[mon]
name=mon
baseurl=ftp://192.168.2.254/ceph/MON
gpgcheck=0
[osd]
name=osd
baseurl=ftp://192.168.2.254/ceph/OSD
gpgcheck=0
[tools]
name=tools
baseurl=ftp://192.168.2.254/ceph/Tools
gpgcheck=0" > /etc/yum.repos.d/ceph.repo
yum clean all &> /dev/null
yum repolist &> /dev/null
