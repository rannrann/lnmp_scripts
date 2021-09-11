from env_preparation.config import *
from other_tools.real_check import *
import threading
class git_config(config):
    def __init__(self, passwd, ip_list):
        super(git_config, self).__init__(passwd, ip_list)
    def start(self):
        self.print_info('Start Git Config')
        self.start_ip_and_yum_checking()

        threads = []
        print("-----------------------------Start package installation-------------------------------")
        for ip in self.addresses:
            command = 'rpm -q git git-daemon httpd gitweb'
            th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.master_packages_path, rpm_string,))
            threads.append(th)
        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------Setting services startup when machines power on-------------------------------")
        command = 'systemctl status httpd'
        words = 'enable the httpd.service'
        self.set_enable_for_service(self.addresses, command, self.git_service_enable_path, services_check, words)
        if not self.process_status:
            print("Pleace check these host")
            return

        # self.close_ssh_con()
        self.print_info('Git Config finished')
if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.2.21']  # ,'192.168.2.13'
    g = git_config(passwd, ip)
    g.start()