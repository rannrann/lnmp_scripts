from env_preparation.mythread import *
from remote_host.ssh_connection import *
from remote_host.sftp_document import *
from other_tools.real_check import *
import threading

import re
class web_config:
    def __init__(self,passwd,ip_list):
        self.addresses = tuple(ip_list)
        self.passwd = passwd
        self.ssh_con = []
        self.con_status= []
        self.ip_con = {}
        self.process_status = True
        self.handover = self.addresses[0]
        self.path_head = '/root/'
        self.local_repo_creator_path = '../scripts/local_repo_creator.sh'
        self.nginx_path = '/linux-soft/2/lnmp_soft/nginx-1.12.2.tar.gz'
        self.nginx_service_creator_path = '../scripts/nginx_service_creator.sh'
        self.nginx_conf_advisor_path = '../scripts/nginx_conf_advisor.sh'
        self.wordpress_path = '/linux-soft/2/lnmp_soft/wordpress.zip'
        self.handover_packages_path = '../scripts/handover_packages.sh'
        self.web_packages_path = '../scripts/web_packages.sh'
        self.nginx_installer_path = '../scripts/nginx_installer.sh'
        self.handover_service_enable_path = '../scripts/handover_service_enable.sh'
        self.web_service_enable_path = '../scripts/web_service_enable.sh'
        self.python_repo_creator_path = '../scripts/python_repo_creator.sh'
        self.pymysql_installer_path = '../scripts/pymysql_installer.sh'
        self.config_mysql_path = '../scripts/config_mysql_on_web.py'
        self.mysql_env_check_path = '../scripts/mysql_env_check_on_handover.py'
        self.lock = threading.RLock()

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

    def nginx_installation(self, ip, command, script_path, check_func):
        flag, failname = self.execute_script_for_one(ip, command, script_path, check_func)
        if flag:
            print(' nginx is ready')
            self.ip_con[ip].ssh_client.exec_command('rm -rf /root/nginx*')
        else:
            print(' failed to install nginx')
            self.process_status = False

    def modify_nginx_conf(self, ip, command, script_path, check_func):
        flag, filename = self.execute_script_for_one(ip, command, script_path, check_func)
        if flag:
            print(' nginx successfully recognized a php page')
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
            self.ip_con[ip].ssh_client.exec_command('rm -rf /usr/local/nginx/html/test.php')
        else:
            print(' nginx failed to recognize a php page')
            self.process_status = False

    def set_enable_for_service(self, ip, command, script_path, check_func):
        flag, filename = self.execute_script_for_one(ip, command, script_path, check_func)
        if flag:
            print(" The services the project needs are enabled")
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
        else:
            print(" There are some services can not be enabled and started")
            self.process_status = False


    #---------------------------------------------follow methods only for self.handover----------------------------------------------
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

    def config_mariadb(self, ip, command, script_path, check_script_path,check_func):
        flag, files = self.execute_py_script_for_one(ip, command, script_path, check_script_path,check_func)
        if flag:
            print(" mariadb is ready")
            for file in files:
                self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + file)
        else:
            print(" failed to config mariadb")
            self.process_status = False

    def deploy_wordpress(self, ip, command, file_path, script_path, check_func):
        filename = file_path.split('/')[-1]
        remote_path = self.path_head + filename
        sftp_document(ip, self.passwd, file_path, remote_path)
        flag, filename = self.execute_script_for_one(ip, command, script_path, check_func)
    # ---------------------------------------------above methods only for self.handover----------------------------------------------
    def start_ip_check(self):
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

    def start_yum_local_repository_check(self):
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
    def start_packages_installation(self):
        threads = []
        print("-----------------------------Start package installation-------------------------------")
        for ip in self.addresses:
            if ip == self.handover:
                command = 'rpm -q gcc openssl-devel pcre-devel mariadb mariadb-server mariadb-devel php php-mysql php-fpm unzip'
                # pit = packages_installation_Thread(self, self.lock,ip,command,self.handover_packages_path,rpm_string)
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.handover_packages_path, rpm_string,))
            else:
                command = 'rpm -q gcc openssl-devel pcre-devel mariadb-devel php php-mysql php-fpm'
                # 不要想着在线程里面创建自己的线程对象，会报错
                # pit = packages_installation_Thread(self, self.lock, ip, command, self.web_packages_path, rpm_string)
                # 可以再线程中再生成一个线程对象，加快代码执行速度
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.web_packages_path, rpm_string,))

            # threads.append(pit)
            threads.append(th)
        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("Pleace check these host")
            return

    def start_nginx_installation(self):
        threads = []
        print("-----------------------------Start nginx installation-------------------------------")
        command = "ls /usr/local/nginx | wc -l"
        nginx_fail_ip = self.check_it(self.addresses, command, nginx_check)
        for ip in nginx_fail_ip:
            self.trans_file(ip, self.nginx_path)
            # self.nginx_installation(ip, command, self.nginx_installer_path, nginx_check)
            th = threading.Thread(target=self.nginx_installation,
                                  args=(ip, command, self.nginx_installer_path, nginx_check,))
            threads.append(th)

        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("\tPleace check these host")
            return
        else:
            print("\tNginx for all hosts is ready")

    def start_create_nginx_service(self):
        print("-----------------------------Creating nginx.service-------------------------------")
        command = 'ls /usr/lib/systemd/system/nginx.service'
        words = 'create the nginx.service'
        nginx_service_fail_ip = self.execute_script_for_many(self.addresses, command, self.nginx_service_creator_path,
                                                             ls_string, words)
        try:
            if nginx_service_fail_ip:
                raise SystemExit("\tPlease check these hosts if nginx.service exists")
            else:
                print("\tAll web hosts had the nginx.service")
        except Exception as e:
            print(e)
            return

    def start_advise_nginx_conf(self):
        print("-----------------------------modify nginx.conf to recognize php pages-------------------------------")
        for ip in self.addresses:
            command = 'curl ' + ip + '/test.php'
            self.modify_nginx_conf(ip, command, self.nginx_conf_advisor_path, php_page_check)
        if not self.process_status:
            print("\tPlease check these hosts!")
            return
        else:
            print('\tAll hosts can recognize php pages')

    def start_set_enable_to_service(self):
        print(
            "-----------------------------Setting services startup when machines power on-------------------------------")
        for ip in self.addresses:
            if ip == self.handover:
                command = 'systemctl status php-fpm nginx mariadb'
                self.set_enable_for_service(ip, command, self.handover_service_enable_path, services_check)
            else:
                command = 'systemctl status php-fpm nginx'
                self.set_enable_for_service(ip, command, self.web_service_enable_path, services_check)

        if not self.process_status:
            print("Pleace check these host")
            return
    def start_install_python(self):
        print("-----------------------------start installing python3-------------------------------")
        command = 'rpm -q python3'
        self.install_python3(self.handover, command, self.python_repo_creator_path, rpm_string)
        if not self.process_status:
            print("Pleace check these host")
            return
    def start_install_pymysql(self):
        print("-----------------------------start installing pymysql-------------------------------")
        command = 'pip3 show pymysql'
        self.install_pymysql(self.handover, command, self.pymysql_installer_path, module_check)
        if not self.process_status:
            print("Pleace check these host")
            return
    def start_config_mariadb(self):
        print("-----------------------------start configing mariadb-------------------------------")
        with open(self.config_mysql_path, 'r') as r:
            content_lines = []
            for lines in r.readlines():
                result = re.findall(r'\'\'', lines)
                if result:
                    content_lines.append(lines.replace('\'\'', '\'' + self.handover + '\'', 1))
                else:
                    content_lines.append(lines)
            with open(self.config_mysql_path, 'w') as w:
                for lines in content_lines:
                    w.write(lines)
        command = "python3 " + self.path_head + self.mysql_env_check_path.split('/')[-1]
        self.config_mariadb(self.handover, command, self.config_mysql_path, self.mysql_env_check_path, mysql_check)
        if not self.process_status:
            print("Pleace check these host")
            return

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
        for ip in self.addresses:
            if ip == self.handover:
                command = 'rpm -q gcc openssl-devel pcre-devel mariadb mariadb-server mariadb-devel php php-mysql php-fpm unzip'
                # pit = packages_installation_Thread(self, self.lock,ip,command,self.handover_packages_path,rpm_string)
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.handover_packages_path, rpm_string,))
            else:
                command = 'rpm -q gcc openssl-devel pcre-devel mariadb-devel php php-mysql php-fpm'
                # 不要想着在线程里面创建自己的线程对象，会报错
                # pit = packages_installation_Thread(self, self.lock, ip, command, self.web_packages_path, rpm_string)
                # 可以再线程中再生成一个线程对象，加快代码执行速度
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.web_packages_path, rpm_string,))

            # threads.append(pit)
            threads.append(th)
        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("Pleace check these host")
            return

        threads = []
        print("-----------------------------Start nginx installation-------------------------------")
        command = "ls /usr/local/nginx | wc -l"
        nginx_fail_ip = self.check_it(self.addresses, command, nginx_check)
        for ip in nginx_fail_ip:
            self.trans_file(ip, self.nginx_path)
            # self.nginx_installation(ip, command, self.nginx_installer_path, nginx_check)
            th = threading.Thread(target=self.nginx_installation,
                                  args=(ip, command, self.nginx_installer_path, nginx_check,))
            threads.append(th)

        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("\tPleace check these host")
            return
        else:
            print("\tNginx for all hosts is ready")

        print("-----------------------------Creating nginx.service-------------------------------")
        command = 'ls /usr/lib/systemd/system/nginx.service'
        words = 'create the nginx.service'
        nginx_service_fail_ip = self.execute_script_for_many(self.addresses, command, self.nginx_service_creator_path,
                                                             ls_string, words)
        try:
            if nginx_service_fail_ip:
                raise SystemExit("\tPlease check these hosts if nginx.service exists")
            else:
                print("\tAll web hosts had the nginx.service")
        except Exception as e:
            print(e)
            return

        print("-----------------------------modify nginx.conf to recognize php pages-------------------------------")
        for ip in self.addresses:
            command = 'curl ' + ip + '/test.php'
            self.modify_nginx_conf(ip, command, self.nginx_conf_advisor_path, php_page_check)
        if not self.process_status:
            print("\tPlease check these hosts!")
            return
        else:
            print('\tAll hosts can recognize php pages')

        print("-----------------------------Setting services startup when machines power on-------------------------------")
        for ip in self.addresses:
            if ip == self.handover:
                command = 'systemctl status php-fpm nginx mariadb'
                self.set_enable_for_service(ip, command, self.handover_service_enable_path, services_check)
            else:
                command = 'systemctl status php-fpm nginx'
                self.set_enable_for_service(ip, command, self.web_service_enable_path, services_check)

        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start installing python3-------------------------------")
        command = 'rpm -q python3'
        self.install_python3(self.handover, command, self.python_repo_creator_path, rpm_string)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start installing pymysql-------------------------------")
        command = 'pip3 show pymysql'
        self.install_pymysql(self.handover, command, self.pymysql_installer_path, module_check)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start configing mariadb-------------------------------")
        with open(self.config_mysql_path, 'r') as r:
            content_lines = []
            for lines in r.readlines():
                result = re.findall(r'wordpress@\'\'', lines)
                print(result)
                if result:
                    content_lines.append(lines.replace('\'\'', '\'' + self.handover + '\'', 1))
                else:
                    content_lines.append(lines)
            with open(self.config_mysql_path, 'w') as w:
                for lines in content_lines:
                    w.write(lines)
        command = "python3 " + self.path_head + self.mysql_env_check_path.split('/')[-1]
        self.config_mariadb(self.handover, command, self.config_mysql_path, self.mysql_env_check_path, mysql_check)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start deploying wordpress-------------------------------")


        for con in self.ssh_con:
            con.close_ssh_client()


if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.2.11','192.168.2.12','192.168.2.13']
    # w = web_config(passwd,ip)
    # w.start()

    # con = ssh_connection(passwd, ip[0])
    # stdin, stdout, stderr = con.ssh_client.exec_command("python3 /root/mysql_env_check_on_handover.py")
    # s = stdout.read().decode()
    # ss = stderr.read().decode()
    # print(mysql_check(s))
    # print("stdout:",s)
    # print("stderr:",ss)
    # con.close_ssh_client()









