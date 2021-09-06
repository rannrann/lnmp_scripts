from env_preparation.config import *
from other_tools.real_check import *
import threading
import time
class ceph_config(config):
    def __init__(self, passwd, ip_list):
        super(ceph_config, self).__init__(passwd, ip_list)
        self.manager = self.addresses[0]
        self.hostnames = None

    def execute_script_for_ceph(self, ip, command, script_path, check_func, pos_variadlb):
        filename = script_path.split('/')[-1]
        remote_path = self.path_head + filename
        sftp_document(ip, self.passwd, script_path, remote_path)
        # 必须要有stdin, stdout, stderr= …… 而且必须要调用参数，因为如果只是单纯执行脚本，real_check.py的函数会先执行
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command("bash " + remote_path + " "+ pos_variadlb)
        print('\t' + ip + ":", stdout.read().decode(), end='')
        time.sleep(10)
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command(command)
        flag_value = check_func(stdout.read().decode())
        return flag_value, filename

    def expect_script_with_pos_variable(self, ip, script_path, pos_variadlbs):
        filename = script_path.split('/')[-1]
        remote_path = self.path_head + filename
        sftp_document(ip, self.passwd, script_path, remote_path)
        file_type = script_path.split('.')[-1]
        variadles = ' '.join(pos_variadlbs)
        stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command(self.type[file_type] + remote_path + " " + variadles)
        print('\t' + ip + ":", 'success to receive a secret key' if stdout.read() else 'failed to receive a secret key')
        return filename


    def set_chrony(self, ip, command, script_path, check_func, pos_variadlb):
        flag, filename = self.execute_script_for_ceph(ip, command, script_path, check_func, pos_variadlb)
        if flag:
            print(" chrony is ready")
            self.ip_con[ip].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
        else:
            print(" failed to set chrony.conf")
            self.process_status = False

    def start(self):
        self.start_ip_and_yum_checking()
        print("-----------------------------Start yum ceph repository checking-------------------------------")
        command = 'yum provides ceph-mon'
        fail_ip = self.check_it(self.addresses, command, ceph_check)
        words = "create the /etc/yum.repos.d/ceph.repo"
        ceph_fail_ip = self.execute_script_for_many(fail_ip, command, self.ceph_repo_creator_path,
                                                    ceph_check, words)
        try:
            if ceph_fail_ip:
                raise SystemExit("\tPlease check these hosts")
            else:
                print("\tCeph for all hosts is ready")
        except Exception as e:
            print('\t' + e)
            return

        threads = []
        print("-----------------------------Start package installation-------------------------------")
        for ip in self.addresses:
            if ip == self.manager:
                command = 'rpm -q ceph-mon ceph-osd ceph-mds ceph-deploy'
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.manager_packages_path,rpm_string,))
            else:
                command = 'rpm -q ceph-mon ceph-osd ceph-mds'
                th = threading.Thread(target=self.packages_installation,
                                      args=(ip, command, self.ceph_packages_path, rpm_string,))
            threads.append(th)
        for t in threads:
            t.start()
            t.join()
        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------Start initializing /etc/hosts-------------------------------")
        command = 'cat /etc/hosts | wc -l'
        words = 'initialize /etc/hosts'
        fail_ip = self.execute_script_for_many(self.addresses, command, self.hosts_initialize_path, hosts_initial_check,
                                               words)
        try:
            if fail_ip:
                raise SystemExit("\tPlease check these hosts if /etc/hosts is initialized")
            else:
                print("\t/etc/hosts for all ceph hosts is initialized")
        except Exception as e:
            print(e)
            return

        print("-----------------------------Start modifying /etc/hosts-------------------------------")
        ip_hostname = {}
        for ip in self.addresses:
            stdin, stdout, stderr = self.ip_con[ip].ssh_client.exec_command('hostname')
            resu = re.findall(r'\w+', stdout.read().decode())
            ip_hostname[ip] = resu[0]

        self.hostnames = [hostname for ip, hostname in ip_hostname.items()]

        list = [i+" "+j+"\n" for i, j in ip_hostname.items()]
        str = ''.join(list)

        with open(self.hosts_creator_path,'r') as r:
            content=[]
            for line in r.readlines():
                if re.findall(r'echo', line):
                    content.append(line.replace('""','\"'+str+'\"'))
                else:
                    content.append(line)
            with open(self.hosts_creator_path, 'w') as w:
                for line in content:
                    w.write(line)

        command = 'cat /etc/hosts | wc -l'
        words = 'modify the /etc/hosts'
        hosts_fail_ip = self.execute_script_for_many(self.addresses, command, self.hosts_creator_path, hosts_check, words)
        try:
            if hosts_fail_ip:
                raise SystemExit("\tPlease check these hosts if /etc/hosts is modified")
            else:
                print("\t/etc/hosts for all hosts is ready")
        except Exception as e:
            print(e)
            return

        print("-----------------------------Start modifying /etc/chrond.conf-------------------------------")
        threads = []
        for ip in self.addresses:
            if ip == self.manager:
                command = 'echo nothing &> /dev/null'
                pos_variadlb = self.manager.split('.')[-2]
                th = threading.Thread(target=self.set_chrony,
                                      args=(ip, command, self.modify_chronyd_conf_on_manager_path, no_check,pos_variadlb,))
            else:
                command = 'chronyc sources -v'
                pos_variadlb = self.manager
                th = threading.Thread(target=self.set_chrony,
                                      args=(ip, command, self.modify_chronyd_conf_on_ceph_path, chrony_check,pos_variadlb,))
            threads.append(th)
        for t in threads:
            t.start()
            t.join()

        if not self.process_status:
            print("Pleace check these host")
            return

        print("-----------------------------Start creating secret key on manager and send it to other hosts-------------------------------")
        stdin, stdout, stderr = self.ip_con[self.manager].ssh_client.exec_command("rm -rf /root/.ssh/id_rsa; ssh-keygen -f /root/.ssh/id_rsa -N '' &> /dev/null")
        print('\t' + self.manager + ":", stdout.read().decode(), "created a secrete key")
        for i in range(1, len(self.addresses)):
            stdin, stdout, stderr = self.ip_con[self.addresses[i]].ssh_client.exec_command("rm -rf /root/.ssh/authorized_keys")
            print('\t' + self.addresses[i] + ":", stdout.read().decode(),end='')
            filename = self.expect_script_with_pos_variable(self.manager, self.autocopy_path, [self.addresses[i], self.passwd])
            self.ip_con[self.manager].ssh_client.exec_command('rm -rf '+self.path_head + filename)


        print("-----------------------------Start deploying ceph monitor-------------------------------")
        command = "ceph -s"
        refer_num, filename = self.execute_script_for_one(self.manager, command, self.deploy_ceph_mon_path, mon_number)
        if refer_num == len(self.addresses):
            print(" ceph-mon for all hosts is ready")
            self.ip_con[self.manager].ssh_client.exec_command('rm -rf ' + self.path_head + filename)
        else:
            print(" failed to deploy ceph-mon. Please check")
            return

        for con in self.ssh_con:
            con.close_ssh_client()


if __name__ == '__main__':
    passwd = '123456'
    ip = ['192.168.2.41', '192.168.2.42', '192.168.2.43']
    c = ceph_config(passwd, ip)
    c.start()
    # con = ssh_connection(passwd, ip[1])
    # stdin, stdout, stderr = con.ssh_client.exec_command("ceph -s")
    # result = re.findall(r'\d+ mons',stdout.read().decode())
    # subresult = re.findall(r'\d+',result[0])
    # print(int(subresult[0]))
    # print("stdout:",stdout.read().decode())
    # print("stderr:", stderr.read().decode())
    # con.close_ssh_client()

    # dict={"1111":"one","2222":"two"}
    # s = [i+ j +"\n" for i, j in dict.items()]
    # s2=''.join(s)
    # print(s2)





