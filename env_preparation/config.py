from remote_host.ssh_connection import *
from remote_host.sftp_document import *
class config:
    def __init__(self,passwd,ip_list):
        self.addresses = tuple(ip_list)
        self.passwd = passwd
        self.ssh_con = []
        self.con_status = []
        self.ip_con = {}
        self.process_status = True
        self.path_head = '/root/'
        self.ceph_repo_creator_path = '../scripts/ceph_repo_creator.sh'
        self.config_mysql_on_database_path = '../scripts/config_mysql_on_database.py'
        self.config_mysql_on_web_path = '../scripts/config_mysql_on_web.py'
        self.database_packages_path = '../scripts/database_packages.sh'
        self.database_serivice_enable_path = '../scripts/database_serivice_enable.sh'
        self.deploy_wordpress_path = '../scripts/deploy_wordpress.sh'
        self.handover_packages_path = '../scripts/handover_packages.sh'
        self.handover_service_enable_path = '../scripts/handover_service_enable.sh'
        self.local_repo_creator_path = '../scripts/local_repo_creator.sh'
        self.mysql_env_check_on_database_path = '../scripts/mysql_env_check_on_database.py'
        self.mysql_env_check_on_handover_path = '../scripts/mysql_env_check_on_handover.py'
        self.nginx_conf_advisor_path = '../scripts/nginx_conf_advisor.sh'
        self.nginx_installer_path = '../scripts/nginx_installer.sh'
        self.nginx_service_creator_path = '../scripts/nginx_service_creator.sh'
        self.pymysql_installer_path = '../scripts/pymysql_installer.sh'
        self.python_repo_creator_path = '../scripts/python_repo_creator.sh'
        self.test_php_path = '../scripts/test_php.sh'
        self.web_packages_path = '../scripts/web_packages.sh'
        self.web_service_enable_path = '../scripts/web_service_enable.sh'
        self.nginx_path = '/linux-soft/2/lnmp_soft/nginx-1.12.2.tar.gz'
        self.wordpress_path = '/linux-soft/2/lnmp_soft/wordpress.zip'

    def ssh_con_creator(self):
        return tuple([ssh_connection(self.passwd,i) for i in self.addresses])

    def trans_file(self, ip, local_path):
        filename = local_path.split('/')[-1]
        remote_path = self.path_head + filename
        sftp_document(ip, self.passwd, local_path, remote_path)

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
            print('\t' + ip + ":", stdout.read().decode(), end='')
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
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command("bash " + remote_path)
        print('\t' + ip + ":", stdout.read().decode(), end='')
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command(command)
        flag_value = check_func(stdout.read().decode())
        return flag_value, filename

    def execute_py_script_for_one(self, ip, command, script_path, check_script_path, check_func):
        filename = []
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

    def install_python3(self, ip, command, script_path, check_func):
        flag_num, filename = self.execute_script_for_one(ip, command, script_path, check_func)
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