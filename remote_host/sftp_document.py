import paramiko
class sftp_document:
    def __init__(self,ip,passwd,local_path,remote_path):
            self.ip = ip
            self.username = "root"
            self.passwd = passwd
            self.send_documents(local_path,remote_path)


    def send_documents(self,local_path,remote_path):
        try:
            tran = paramiko.Transport(self.ip,22)
            tran.connect(username=self.username, password=self.passwd)
            sftp = paramiko.SFTPClient.from_transport(tran)
            sftp.put(local_path,remote_path)
            tran.close()
        except Exception as e:
            print("There is some problem with transfering a document:",e)