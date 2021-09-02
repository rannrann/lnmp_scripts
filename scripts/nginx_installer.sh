#!/bin/bash
tar -xf /root/nginx-1.12.2.tar.gz -C /root
cd /root/nginx-1.12.2
 ./configure &> /dev/null
 make &> /dev/null
 make install &> /dev/null