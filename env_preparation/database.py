from env_preparation.config import *
from other_tools.real_check import *
import threading
class database_config(config):
    def __init__(self, passwd, ip_list):
        super(database_config, self).__init__(passwd, ip_list)


    def set_enable_for_service(self, addresses, command, script_path, check_func, words):
        fail_ip = self.execute_script_for_many(addresses, command, script_path, check_func, words)
        if fail_ip:
            self.process_status = False


    def start(self):
        print("-----------------------------Start ip checking-------------------------------")
        self.ssh_con = self.ssh_con_creator()
        self.con_status = [i.flag for i in self.ssh_con]
        for i in self.con_status:
            if not i:
                print("\tplease check these ip")
                return
        else:
            print("\tAll addresses are reachable")
            for i in range(len(self.addresses)):
                self.ip_con[self.addresses[i]] = self.ssh_con[i]

        print("-----------------------------Start yum local repository checking-------------------------------")
        command = 'yum clean all; yum repolist'
        yum_fail_ip = self.check_it(self.addresses, command, yum_repolist_string)
        for ip in yum_fail_ip:
            print("\tset a yum repository on", ip)
        words = "create the /etc/yum.repos.d/local.repo"
        yum_fail_ip = self.execute_script_for_many(yum_fail_ip, command, self.local_repo_creator_path,
                                                   yum_repolist_string, words)
        try:
            if yum_fail_ip:
                raise SystemExit("\tPlease check these hosts")
            else:
                print("\tYum for all hosts is ready")
        except Exception as e:
            print('\t' + e)
            return

        threads = []
        print("-----------------------------Start package installation-------------------------------")
        command = "rpm -q  mariadb mariadb-server mariadb-devel"
        for ip in self.addresses:
            th = threading.Thread(target=self.packages_installation,
                                  args=(ip, command, self.database_packages_path, rpm_string,))
            threads.append(th)
        for thread in threads:
            thread.start()
            thread.join()
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------Setting services startup when machines power on-------------------------------")
        command = 'systemctl status mariadb'
        words = 'enable the mariadb.service'
        self.set_enable_for_service(self.addresses, command, self.database_serivice_enable_path, services_check, words)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start installing python3-------------------------------")
        command = 'rpm -q python3'
        for ip in self.addresses:
            self.install_python3(ip, command, self.python_repo_creator_path, rpm_string)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start installing pymysql-------------------------------")
        command = 'pip3 show pymysql'
        for ip in self.addresses:
            self.install_pymysql(ip, command, self.pymysql_installer_path, module_check)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start configing mariadb-------------------------------")
        command = "python3 " + self.path_head + self.mysql_env_check_on_database_path.split('/')[-1]
        for ip in self.addresses:
            self.config_mariadb(ip, command, self.config_mysql_on_database_path, self.mysql_env_check_on_database_path, mysql_check)
        if not self.process_status:
            print("Pleace check these host")
            return


        for con in self.ssh_con:
            con.close_ssh_client()

if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.2.21']  # ,'192.168.2.13'
    b = database_config(passwd, ip)
    b.start()
