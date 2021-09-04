#!/bin/bash
ssh-keygen -f /root/.ssh/id_rsa -N '' &> /dev/null
for i in 41 42 43
do
  ssh-copy-id 192.168.2.$i &> /dev/null
done