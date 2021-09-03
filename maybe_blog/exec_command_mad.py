from remote_host.ssh_connection import *
from remote_host.sftp_document import *
passwd = '123456'
ip = ['192.168.2.11','192.168.2.12'] #,'192.168.2.13'
# w = web_config(passwd,ip)
# w.start()

con = ssh_connection(passwd, ip[0])
stdin, stdout, stderr = con.ssh_client.exec_command("ll /usr/local/nginx/html/")
s = stdout.read().decode()# stdout已经 用了一次
ss = stderr.read().decode()

print("stdout:", stdout.read().decode()) #不能输出,只能用一次
print("stdout:", s) #能输出
con.close_ssh_client()