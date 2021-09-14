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

        threads = [ceph_th, web_th, database_th,proxy_th, git_th]#
        for thread in threads:
            thread.start()
            thread.join()

    def close_ssh_con(self):
        self.web.close_ssh_con()
        self.git.close_ssh_con()
        self.database.close_ssh_con()
        self.proxy.close_ssh_con()
        self.ceph.close_ssh_con()

    def test_roundrobin(self,web_ip, proxy_ip):
        access_ip = self.web.get_last_ip_from_access_log(web_ip)
        return True if proxy_ip == access_ip else False

    def start(self):
        self.web.start_ip_and_yum_checking()
        self.proxy.start_ip_and_yum_checking()
        # self.database.start_ip_and_yum_checking()
        # self.ceph.start_ip_and_yum_checking()
        # print("---------------------------------------stop nginx php-fpm mariadb on web hosts-----------------------------------------")
        #
        # command = 'systemctl status nginx php-fpm'
        # words = 'stop services'
        # fail_ip = self.web.execute_script_for_many(self.web.addresses, command, self.web.stop_web_services_path, stoped_services_check, words)
        # if fail_ip:
        #     return
        #
        # print("---------------------------------------export wordpress database from handover host-----------------------------------------")
        # command='ls /root/wordpress.bak'
        # flag, filename = self.web.execute_script_for_one(self.web.handover, command, self.web.export_database_path, ls_string)
        # if flag:
        #     print(" successed to export wordpress database")
        #     self.web.ip_con[self.web.handover].ssh_client.exec_command('rm -rf ' + self.web.path_head + filename)
        # else:
        #     print(" failed to export wordpress database")
        #     return
        #
        # print("---------------------------------------tansfer a data file to database server-----------------------------------------")
        # filename = self.web.expect_script_with_pos_variable(self.web.handover, self.web.autoscp_path, [self.database.addresses[0], self.web.path_head+'wordpress.bak', self.web.path_head, self.ceph.passwd], 'transfer the wordpress.bak to database server')
        # self.web.ip_con[self.web.handover].ssh_client.exec_command('rm -rf ' + self.web.path_head + filename)
        # self.web.ip_con[self.web.handover].ssh_client.exec_command('rm -rf ' + self.web.path_head + 'wordpress.bak')
        #
        # print("---------------------------------------stop mariadb server on handover-----------------------------------------")
        # command = 'systemctl status mariadb'
        # flag, filename = self.web.execute_script_for_one(self.web.handover, command, self.web.stop_mariadb_service_path,
        #                                            stoped_services_check)
        # if flag:
        #     print(" successed to stop mariadb service")
        #     self.web.ip_con[self.web.handover].ssh_client.exec_command("rm -rf "+self.web.path_head+filename)
        # else:
        #     print(" failed to stop mariadb service")
        #     return
        #
        # print("---------------------------------------import data to database on database server-----------------------------------------")
        # command = 'bash ' + self.database.path_head + self.database.mysql_check_on_database_path.split('/')[-1]
        # flag, filename = self.database.execute_two_scripts_for_one(self.database.addresses[0], command, self.database.import_data_path, self.database.mysql_check_on_database_path, data_check)
        # if flag:
        #     print(" successed to import wordpress.bak")
        #     for f in filename:
        #         self.database.ip_con[self.database.addresses[0]].ssh_client.exec_command("rm -rf "+self.database.path_head+f)
        # else:
        #     print(" failed to import wordpress.bak")
        #     return
        #
        # print("---------------------------------------modify wordpress conf-----------------------------------------")
        # variadle = [self.database.addresses[0]]
        # flag, filename = self.web.check_it(self.web.handover, self.web.mysql_check_on_handover2_path, data_check, variadle)
        # if flag:
        #     print(" successed to access to "+self.database.addresses[0])
        #     self.web.ip_con[self.web.handover].ssh_client.exec_command('rm -rf ' + self.web.path_head + filename)
        # else:
        #     print(" failed to access to " + self.database.addresses[0])
        #     return
        #
        # command = "echo a &> /dev/null"
        # flag, filename = self.web.execute_script_for_one(self.web.handover, command, self.web.modify_wordpress_conf_path, no_check)
        # self.web.ip_con[self.web.handover].ssh_client.exec_command('rm -rf ' + self.web.path_head + filename)
        # print(" wp-config.php has been modified")
        #
        # print("---------------------------------------mount ceph cluster on /usr/local/nginx/html-----------------------------------------")
        # command = "echo a &> /dev/null"
        # flag, filename = self.web.execute_script_for_one(self.web.handover, command,
        #                                                  self.web.pack_pages_path, no_check)
        # self.web.ip_con[self.web.handover].ssh_client.exec_command('rm -rf ' + self.web.path_head + filename)
        # print(" All pages in /usr/locat/nginx/html has been packed as /usr/local/nginx/html.tar.gz")
        #
        # stdin, stdout, stderr = self.web.ip_con[self.web.handover].ssh_client.exec_command("rm -rf /usr/locat/nginx/html/*")
        # print("\t"+self.web.handover+stdout.read().decode()+": delete all file in /usr/locat/nginx/html")
        #
        # stdin, stdout, stderr = self.ceph.ip_con[self.ceph.manager].ssh_client.exec_command("cat /etc/ceph/ceph.client.admin.keyring")
        # resu = re.search(r'(key = )(.*)', stdout.read().decode())
        # passwd = resu.group(2).strip()
        #
        # command = "mount -a"
        # for ip in self.web.addresses:
        #     flag, filename = self.web.execute_script_for_one(ip, command, self.web.mount_ceph_path, mount_check, [self.ceph.manager, passwd])
        #     if flag:
        #         print(' successed to mount ceph cluster on /usr/local/nginx/html')
        #         self.web.ip_con[ip].ssh_client.exec_command("rm -rf "+self.web.path_head+filename)
        #     else:
        #         print(' failed to mount ceph cluster on /usr/local/nginx/html')
        #         self.process_status = False
        #
        # if not self.process_status:
        #     print("Please check these ip")
        #     return
        #
        # print("---------------------------------------unpack html.tar.gz to /usr/local/nginx/html-----------------------------------------")
        # command = "ls /usr/local/nginx/html/"
        # flag, filename = self.web.execute_script_for_one(self.web.handover, command, self.web.unpack_pages_path, ls_string)
        # if flag:
        #     print(" successed to unpack html.tar.gz")
        #     self.web.ip_con[self.web.handover].ssh_client.exec_command("rm -rf "+self.web.path_head+filename)
        # else:
        #     print(" failed to unpack html.tar.gz")
        #     return
        #
        # print("---------------------------------------start nginx service of all web hosts-----------------------------------------")
        # command = "systemctl status nginx php-fpm"
        # for ip in self.web.addresses:
        #     stdin, stdout, stderr = self.web.ip_con[ip].ssh_client.exec_command("systemctl start nginx php-fpm")
        #     if stdout.read().decode():
        #         print("\t"+ip+": can't start nginx, php-fpm")
        # fail_ip = self.web.check_all(self.web.addresses, command, services_check)
        # if fail_ip:
        #     for ip in fail_ip:
        #         print('\t'+ip+':'+' failed to start nginx and php-fpm')
        #     return
        # else:
        #     print("\tAll web hosts start nginx and php-fpm")
        #


        print("---------------------------------------modify /etc/haproxy/haproxy.cfg-----------------------------------------")
        ip_hostname={}
        for ip in self.web.addresses:
            stdin, stdout, stderr = self.web.ip_con[ip].ssh_client.exec_command('hostname')
            resu = re.findall(r'\w+', stdout.read().decode())
            ip_hostname[ip] = resu[0]
        content=['#!/bin/bash\n', 'echo "listen wordpress *:80\n', '  balance roundrobin\n']
        for ip, hostname in ip_hostname.items():
            content.append('  server '+hostname+' '+ip+':80 check\n')
        content.append('" >> /etc/haproxy/haproxy.cfg')
        with open(self.web.modify_haproxy_conf_path,'w') as w:
            for line in content:
                w.write(line)


        print("---------------------------------------start haproxy service-----------------------------------------")

        command = 'systemctl enable haproxy --now; systemctl status haproxy'
        words = 'start haproxy service'
        fail_ip = self.proxy.execute_script_for_many(self.proxy.addresses, command, self.proxy.modify_haproxy_conf_path, services_check, words)
        if fail_ip:
            print("\tPlease check theses hosts")
            return
        else:
            print("\tHaproxy for all proxy hosts is ready")

        print("---------------------------------------test roundrobin-----------------------------------------")
        filename = self.web.trans_file(self.web.handover, self.web.test_php_path)
        stdin, stdout, stderr = self.web.ip_con[self.web.handover].ssh_client.exec_command('bash '+self.web.path_head + filename)
        print('\t'+self.web.handover+stdout.read().decode()+': test page is ready')

        for proxy_ip in self.proxy.addresses:
            content=['#!/bin/bash\n']
            for _ in self.web.addresses:
                content.append("curl "+proxy_ip+"/test.php &> /dev/null\n")
            with open(self.proxy.test_roundrobin_path,'w') as w:
                for line in content:
                    w.write(line)
            command = "echo a > /dev/null"
            flag, filename = self.proxy.execute_script_for_one(proxy_ip, command, self.proxy.test_roundrobin_path, no_check)
            self.proxy.ip_con[proxy_ip].ssh_client.exec_command("rm -rf "+self.proxy.path_head+filename)
            print()
            for web_ip in self.web.addresses:
                flag = self.test_roundrobin(web_ip, proxy_ip)
                if flag:
                    print('\t'+web_ip+' was accessed')
                else:
                    print('\t' + web_ip + ' was not accessed')

        print("---------------------------------------start keepalived service-----------------------------------------")
        command = 'echo a > /dev/null'
        vip = input("please input a vip for proxy hosts:")
        flag, filename = self.proxy.execute_script_for_one(self.proxy.addresses[0], command,
                                          self.proxy.modify_keepalived_conf_for_master_path,
                                          no_check, [vip])
        print(' successed to modify keepalived.conf')
        self.proxy.ip_con[self.proxy.addresses[0]].ssh_client.exec_command('rm -rf ' + self.proxy.path_head + filename)
        self.proxy.execute_script_for_one(self.proxy.addresses[-1], command,
                                          self.proxy.modify_keepalived_conf_for_backup_path,
                                          no_check, [vip])
        print(' successed to modify keepalived.conf')
        self.proxy.ip_con[self.proxy.addresses[-1]].ssh_client.exec_command('rm -rf ' + self.proxy.path_head + filename)
        for ip in self.proxy.addresses:
            stdin, stdout, stderr = self.proxy.ip_con[ip].ssh_client.exec_command('systemctl enable keepalived --now')
            print('\t'+ip+stdout.read().decode()+': start keepalived service')


        stdin, stdout, stderr = self.proxy.ip_con[self.proxy.addresses[0]].ssh_client.exec_command('systemctl stop keepalived')
        print('\t' + self.proxy.addresses[0] + stdout.read().decode() + ': stop keepalived service')
        stdin, stdout, stderr = self.proxy.ip_con[self.proxy.addresses[0]].ssh_client.exec_command('curl '+vip+'/test.php')
        flag = keepalived_check(stdout.read().decode())
        if flag:
            print("Keepalived running with no problem")
            self.proxy.ip_con[self.proxy.addresses[0]].ssh_client.exec_command('systemctl start keepalived')
        else:
            print("Keepalived running unexpectly. Please check.")

        self.close_ssh_con()

if __name__ == "__main__":
    passwd = '123456'
    web_ip = ['192.168.2.11', '192.168.2.12', '192.168.2.13']
    database_ip = ['192.168.2.21']
    git_ip = ['192.168.2.21']
    proxy_ip = ['192.168.2.5', '192.168.2.6']
    ceph_ip = ['192.168.2.41', '192.168.2.42', '192.168.2.43']
    o = operation('123456')
    o.set_ceph(ceph_ip)
    o.set_web(web_ip)
    o.set_database(database_ip)
    o.set_git(git_ip)
    o.set_proxy(proxy_ip)
    o.env_preparation()
    answer = input("Please complete the installation of wordpress on the "+web_ip[0] +
          ". \nIf you prepare to continue the process, please press y; If you want to stop the process, please press n:")
    if answer == 'y':
        o.start()
    else:
        o.close_ssh_con()

    # o.start()


    # s = ssh_connection(passwd, ceph_ip[0])
    # stdin, stdout, stderr = s.ssh_client.exec_command("cat /etc/ceph/ceph.client.admin.keyring")
    # resu = re.search(r'(key = )(.*)', stdout.read().decode())
    # passwd = resu.group(2).strip()
    # print(passwd)
    # s.close_ssh_client()






