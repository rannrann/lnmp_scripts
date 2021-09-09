#!/bin/bash
cd /root/ceph_cluster
ceph osd pool create cephfs_data 64
ceph osd pool create cephfs_metadata 64
ceph fs new myfs1 cephfs_metadata cephfs_data