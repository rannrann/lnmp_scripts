#!/bin/bash
echo "[mon]
name=mon
baseurl=file:///ceph/MON
gpgcheck=0
[osd]
name=osd
baseurl=file:///ceph/OSD
gpgcheck=0
[tools]
name=tools
baseurl=file:///ceph/Tools
gpgcheck=0" > /etc/yum.repos.d/ceph.repo
yum clean all &> /dev/null
yum repolist &> /dev/null
