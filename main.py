from remote_host import *
from remote_host.sftp_document import sftp_document
from remote_host.ssh_connection import ssh_connection


if __name__ == "__main__":
    pass
    # tran = sftp_document('192.168.2.41','123456','scripts/ceph_repo_creator.sh','/root/ceph_repo_creator.sh')
    # con = ssh_connection('192.168.2.41','123456')
    # con.ssh_client.exec_command("bash /root/ceph_repo_creator.sh")
    # con.close_ssh_client()



