import threading
class myThread(threading.Thread):
    def __init__(self, web_obj, lock):
        threading.Thread.__init__(self)
        self.web_obj = web_obj
        self.lock = lock
    def run(self):
        self.lock.acquire()
        self.web_obj.start_ip_check()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_yum_local_repository_check()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_packages_installation()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_nginx_installation()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_create_nginx_service()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_advise_nginx_conf()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_set_enable_to_service()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_install_python()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_install_pymysql()
        self.lock.release()
        self.lock.acquire()
        self.web_obj.start_config_mariadb()
        self.lock.release()


# def packages_installation(self, ip, command, script_path, check_func):
class packages_installation_Thread(threading.Thread):
    def __init__(self, web_obj, lock, ip, command, script_path, check_func):
        threading.Thread.__init__(self)
        self.web_obj = web_obj
        self.ip = ip
        self.command = command
        self.script_path = script_path
        self.check_func = check_func
        self.lock = lock
    def run(self):
        self.lock.acquire()
        self.web_obj.packages_installation(self.ip, self.command, self.script_path,self.check_func)
        self.lock.release()

class for_one_Thread(threading.Thread):
    pass
