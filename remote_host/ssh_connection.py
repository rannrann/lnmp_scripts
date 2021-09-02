import paramiko
class ssh_connection:
    def __init__(self,passwd,ip,username="root"):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.flag =True
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=self.ip, username=self.username, password=self.passwd, port=22)
        except Exception as e:
            print('\t'+str(e))
            self.flag = False
    def close_ssh_client(self):
        self.ssh_client.close()
