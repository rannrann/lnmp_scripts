lsblk | awk '/^[a-z]+/{print $1" "}'
#vda
#vdb
#vdc

blkid | awk '{print $1}' | awk -F/ '{print $3}'
#vda1: