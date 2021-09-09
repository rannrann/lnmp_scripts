from env_preparation.ceph import *
from env_preparation.git import *
from env_preparation.database import *
from env_preparation.web import *
from env_preparation.proxy import *
import threading
from remote_host.ssh_connection import *
from other_tools.real_check import *
class operation:
    def __init__(self, passwd):
        self.ceph = None
        self.web = None
        self.database = None
        self.proxy = None
        self.git = None
        self.passwd = passwd
        self.process_status = True


    def set_ceph(self, ip_list):
        self.ceph = ceph_config(self.passwd, ip_list)

    def set_web(self, ip_list):
        self.web = web_config(self.passwd, ip_list)

    def set_database(self, ip_list):
        self.database = database_config(self.passwd, ip_list)

    def set_proxy(self, ip_list):
        self.proxy = proxy_config(self.passwd, ip_list)

    def set_git(self, ip_list):
        self.git = git_config(self.passwd, ip_list)

    def env_preparation(self):
        ceph_th = threading.Thread(target=self.ceph.start)
        web_th = threading.Thread(target=self.web.start)
        database_th = threading.Thread(target=self.database.start)
        proxy_th = threading.Thread(target=self.proxy.start)
        git_th = threading.Thread(target=self.git.start)

        threads = [ceph_th, web_th, database_th, proxy_th, git_th]
        for thread in threads:
            thread.start()
            thread.join()

    def close_ssh_con(self):
        pass
    def start(self):
        print("---------------------------------------stop nginx php-fpm mariadb  on web hosts-----------------------------------------")
        for ip in self.web.address:
            if ip == self.web.handover:
                command = 'systemctl status nginx php-fpm mariadb'
                flag, filename = self.web.execute_script_for_one(ip, command, self.stop_handover_services_path, stoped_services_check)
            else:
                command = 'systemctl status nginx php-fpm'
                flag, filename = self.web.execute_script_for_one(ip, command, self.stop_web_services_path, stoped_services_check)
            if flag:
                print(" successed to stop services")
                self.web.ip_con[ip].ssh_client.exec_command("rm -rf "+self.web.path_head+filename)
            else:
                print(" failed to stop services")
                self.process_status = False
        if not self.process_status:
            print("\tPlease check these hosts!")
            return




if __name__ == "__main__":
    passwd = '123456'
    web_ip = ['192.168.2.11', '192.168.2.12', '192.168.2.13']
    database_ip = ['192.168.2.21']
    git_ip = ['192.168.2.21']
    proxy_ip = ['192.168.2.5', '192.168.2.6']
    ceph_ip = ['192.168.2.41', '192.168.2.42', '192.168.2.43']
    # o = operation('123456')
    # o.set_ceph(ceph_ip)
    # o.set_web(web_ip)
    # o.set_database(database_ip)
    # o.set_git(git_ip)
    # o.set_proxy(proxy_ip)
    # o.env_preparation()
    s = ssh_connection(passwd, web_ip[0])
    stdin, stdout, stderr = s.ssh_client.exec_command("systemctl status nginx php-fpm mariadb")
    print(stoped_services_check(stdout.read().decode()))
    s.close_ssh_client()






