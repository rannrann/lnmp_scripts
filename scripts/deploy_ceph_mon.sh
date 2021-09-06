#!/bin/bash
deploy_ceph_mon(){
  rm -rf /root/ceph_cluster
  mkdir /root/ceph_cluster
  cd /root/ceph_cluster
  ceph-deploy new $* &> /dev/null
  ceph-deploy mon create-initial &> /dev/null
}
awk '/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/NR>1' /etc/hosts | awk 'NR>1' | awk '{printf $2" "}' >> /root/deploy_ceph_mon.sh
deploy_ceph_mon