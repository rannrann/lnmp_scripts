from env_preparation.config import *
from other_tools.real_check import *
import threading
class proxy_config(config):
    def __init__(self, passwd, ip_list):
        super(proxy_config,self).__init__(passwd,ip_list)
        self.master = self.addresses[0]

    def start(self):
        self.start_ip_and_yum_checking()

        threads = []
        print("-----------------------------Start package installation-------------------------------")
        for ip in self.addresses:
            if ip == self.master:
                command = 'rpm -q haproxy keepalived bind bind-chroot'
                # pit = packages_installation_Thread(self, self.lock,ip,command,self.handover_packages_path,rpm_string)
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.master_packages_path, rpm_string,))
            else:
                command = 'rpm -q haproxy keepalived'
                # 不要想着在线程里面创建自己的线程对象，会报错
                # pit = packages_installation_Thread(self, self.lock, ip, command, self.web_packages_path, rpm_string)
                # 可以再线程中再生成一个线程对象，加快代码执行速度
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.backup_packages_path, rpm_string,))

            # threads.append(pit)
            threads.append(th)
        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("Pleace check these host")
            return

        for con in self.ssh_con:
            con.close_ssh_client()

        print("proxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxyproxy")

if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.4.5', '192.168.4.6']
    p = proxy_config(passwd,ip)
    p.start()