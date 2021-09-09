from env_preparation.config import *
from other_tools.real_check import *
import threading
class database_config(config):
    def __init__(self, passwd, ip_list):
        super(database_config, self).__init__(passwd, ip_list)





    def start(self):
        self.start_ip_and_yum_checking()

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
        command = 'yum provides python3'
        fail_ip = self.check_it(self.addresses, command, python3_check)
        if fail_ip:
            command = 'rpm -q python3'
            for ip in fail_ip:
                self.install_python3(ip, command, self.python_repo_creator_path, rpm_string)
            if not self.process_status:
                print("Pleace check these host")
                return
        else:
            for ip in self.addresses:
                stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command('yum -y install python3 &> /dev/null')
                print('\t' + ip + ":" + stdout.read().decode() + " python3 is ready")


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

        print("databasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabasedatabase")

if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.2.21']  # ,'192.168.2.13'
    b = database_config(passwd, ip)
    b.start()
