#!/bin/bash
cd /root/ceph_cluster
ceph-deploy disk zap 192.168.2.41:vdc 192.168.2.41:vdb 
ceph-deploy disk zap 192.168.2.42:vdc 192.168.2.42:vdb 
ceph-deploy disk zap 192.168.2.43:vdc 192.168.2.43:vdb 
ceph-deploy osd create 192.168.2.41:vdc 192.168.2.41:vdb 
ceph-deploy osd create 192.168.2.42:vdc 192.168.2.42:vdb 
ceph-deploy osd create 192.168.2.43:vdc 192.168.2.43:vdb 
