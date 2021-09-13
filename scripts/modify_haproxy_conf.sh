#!/bin/bash
echo "listen wordpress *:80
  balance roundrobin
  server web1 192.168.2.11:80 check
  server web2 192.168.2.12:80 check
  server web3 192.168.2.13:80 check
" >> /etc/haproxy/haproxy.cfg