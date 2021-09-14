#!/bin/bash
cd /root/ceph_cluster
ceph-deploy disk zap 192.168.2.41:vdb 192.168.2.41:vdc 
ceph-deploy disk zap 192.168.2.42:vdb 192.168.2.42:vdc 
ceph-deploy disk zap 192.168.2.43:vdb 192.168.2.43:vdc 
ceph-deploy osd create 192.168.2.41:vdb 192.168.2.41:vdc 
ceph-deploy osd create 192.168.2.42:vdb 192.168.2.42:vdc 
ceph-deploy osd create 192.168.2.43:vdb 192.168.2.43:vdc 
