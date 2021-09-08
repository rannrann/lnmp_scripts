from env_preparation.config import *
from other_tools.real_check import *
import threading
import re
class web_config(config):
    def __init__(self,passwd,ip_list):
        super(web_config,self).__init__(passwd,ip_list)
        self.handover = self.addresses[0]

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
        stdin,stdout,stderr = self.ip_con[ip].ssh_client.exec_command('yum provides python3')
        if not python3_check(stdout.read().decode()):
            flag_num, filename = self.execute_script_for_one(ip, command, script_path, check_func)
            if flag_num == 0:
                print(" Python3 is ready")
                self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
            else:
                print(" failed to install python3")
                self.process_status = False
        else:
            stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command('yum -y install python3 &> /dev/null')
            print('\t' + ip + ":"+ stdout.read().decode()+" python3 is ready")

    def deploy_wordpress(self, ip, command, file_path, script_path, check_func):
        filename = file_path.split('/')[-1]
        remote_path = self.path_head + filename
        sftp_document(ip, self.passwd, file_path, remote_path)
        flag, filename = self.execute_script_for_one(ip, command, script_path, check_func)
        if flag:
            print(" please access to", ip)
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + 'wordpress*')
        else:
            print(" failed to deploy wordpress")
            self.process_status = False
    # ---------------------------------------------above methods only for self.handover----------------------------------------------

    def start(self):

        self.start_ip_and_yum_checking()

        threads = []
        print("-----------------------------Start package installation-------------------------------")
        for ip in self.addresses:
            if ip == self.handover:
                command = 'rpm -q gcc openssl-devel pcre-devel mariadb mariadb-server mariadb-devel php php-mysql php-fpm unzip ceph-common'
                # pit = packages_installation_Thread(self, self.lock,ip,command,self.handover_packages_path,rpm_string)
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.handover_packages_path, rpm_string,))
            else:
                command = 'rpm -q gcc openssl-devel pcre-devel mariadb-devel php php-mysql php-fpm ceph-common'
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
        with open(self.config_mysql_on_web_path, 'r') as r:
            content_lines = []
            for line in r.readlines():
                result = re.findall(r'wordpress@\'\'', line)
                if result:
                    content_lines.append(line.replace('\'\'', '\'' + self.handover + '\'', 1))
                else:
                    content_lines.append(line)
            with open(self.config_mysql_on_web_path, 'w') as w:
                for line in content_lines:
                    w.write(line)
        command = "python3 " + self.path_head + self.mysql_env_check_on_handover_path.split('/')[-1]
        self.config_mariadb(self.handover, command, self.config_mysql_on_web_path, self.mysql_env_check_on_handover_path, mysql_check)
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------start deploying wordpress-------------------------------")
        command = 'ls /usr/local/nginx/html/'
        self.deploy_wordpress(self.handover, command, self.wordpress_path, self.deploy_wordpress_path, ls_string)
        if not self.process_status:
            print("Pleace check these host")
            return

        for con in self.ssh_con:
            con.close_ssh_client()



if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.2.11','192.168.2.12','192.168.2.13'] #
    w = web_config(passwd,ip)
    w.start()

    # con = ssh_connection(passwd, ip[0])
    # stdin, stdout, stderr = con.ssh_client.exec_command("yum provides python3")
    # # print("stdout:", stdout.read().decode())
    # resu = re.findall(r'python3',stdout.read().decode())
    # print(True if resu else False)
    # con.close_ssh_client()









