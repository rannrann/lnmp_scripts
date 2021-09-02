from remote_host.ssh_connection import *
from remote_host.sftp_document import *
from other_tools.real_check import *
import threading
class database_config:
    def __init__(self, passwd, ip_list):
        self.addresses = tuple(ip_list)
        self.passwd = passwd
        self.ssh_con = []
        self.con_status = []
        self.ip_con = {}
        self.process_status = True
        self.path_head = '/root/'
        self.local_repo_creator_path = '../scripts/local_repo_creator.sh'
        self.database_packages_path = '../scripts/database_packages.sh'
        self.database_serivice_enable_path = '../scripts/database_serivice_enable.sh'
        self.python_repo_creator_path = '../scripts/python_repo_creator.sh'
        self.pymysql_installer_path = '../scripts/pymysql_installer.sh'
        self.config_mysql_path = '../scripts/config_mysql_on_database.py'
        self.mysql_env_check_path = '../scripts/mysql_env_check_on_database.py'



    def check_it(self, addresses, command, check_func):
        fail_ip = []
        for i in range(len(addresses)):
            stdin, stdout, stderr = self.ssh_con[i].ssh_client.exec_command(command)
            if not check_func(stdout.read().decode()):
                fail_ip.append(self.addresses[i])
        return fail_ip
    def execute_script_for_many(self, addresses, command, script_path, check_func, words):
        fail_ip = []
        filename = script_path.split('/')[-1]
        remote_path = self.path_head + filename
        for ip in addresses:
            sftp_document(ip, self.passwd, script_path, remote_path)
            stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command("bash " + remote_path)
            print('\t' + ip + ":",stdout.read().decode(),end='')
            stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command(command)
            if not check_func(stdout.read().decode()):
                fail_ip.append(ip)
                print(" failed to " + words)
            else:
                print(" successed to " + words)
                self.ip_con[ip].ssh_client.exec_command("rm -rf " + remote_path)
        return fail_ip

    def execute_script_for_one(self, ip, command, script_path, check_func):
        filename = script_path.split('/')[-1]
        remote_path = self.path_head + filename
        sftp_document(ip, self.passwd, script_path, remote_path)
        # 必须要有stdin, stdout, stderr= …… 而且必须要调用参数，因为如果只是单纯执行脚本，real_check.py的函数会先执行
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command("bash "+ remote_path)
        print('\t' + ip + ":",stdout.read().decode(),end='')
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command(command)
        flag_value = check_func(stdout.read().decode())
        return flag_value, filename

    def execute_py_script_for_one(self, ip, command, script_path, check_script_path,check_func):
        filename=[]
        filename.append(script_path.split('/')[-1])
        filename.append(check_script_path.split('/')[-1])
        remote_path = self.path_head + filename[0]
        remote_path2 = self.path_head + filename[1]
        sftp_document(ip, self.passwd, script_path, remote_path)
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command("python3 " + remote_path)
        print('\t' + ip + ":", stdout.read().decode(), end='')
        sftp_document(ip, self.passwd, check_script_path, remote_path2)
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command(command)
        flag_value = check_func(stdout.read().decode())
        return flag_value, filename

    def packages_installation(self, ip, command, script_path, check_func):
        refer_num, filename = self.execute_script_for_one(ip, command, script_path, check_func)
        if refer_num != 0:
            print(str(refer_num)+" packages can't not be installed.")
            self.process_status = False
        else:
            print(' All packages the project needs are installed successfully')
            self.ip_con[ip].ssh_client.exec_command('rm -rf '+self.path_head+filename)

    def set_enable_for_service(self, addresses, command, script_path, check_func, words):
        fail_ip = self.execute_script_for_many(addresses, command, script_path, check_func, words)
        if not fail_ip:
            print(" There are some services can not be enabled and started")
            self.process_status = False
        else:
            print(" The services the project needs are enabled")

    def install_python3(self, ip, command, script_path, check_func):
        flag_num, filename = self.execute_script_for_many(ip, command, script_path, check_func)
        if flag_num == 0:
            print(" Python3 is ready")
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
        else:
            print(" failed to install python3")
            self.process_status = False

    def install_pymysql(self, ip, command, script_path, check_func):
        flag, filename = self.execute_script_for_one(ip, command, script_path, check_func)
        if flag:
            print(" pymysql is ready")
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
        else:
            print(" failed to install pymysql")
            self.process_status = False

    def config_mariadb(self, ip, command, script_path, check_script_path, check_func):
        flag, files = self.execute_py_script_for_one(ip, command, script_path, check_script_path, check_func)
        if flag:
            print(" mariadb is ready")
            for file in files:
                self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + file)
        else:
            print(" failed to config mariadb")
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
                                  args=(ip, command, self.self.database_packages_path, rpm_string,))
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
        command = "python3 " + self.path_head + self.mysql_env_check_path.split('/')[-1]
        for ip in self.addresses:
            self.config_mariadb(ip, command, self.config_mysql_path, self.mysql_env_check_path, mysql_check)
        if not self.process_status:
            print("Pleace check these host")
            return


        for con in self.ssh_con:
            con.close_ssh_client()
