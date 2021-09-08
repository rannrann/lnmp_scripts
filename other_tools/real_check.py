import re

def yum_repolist_string(stdout):
    num = re.search(r'(repolist:)(.*)',stdout)
    num = num.group(2).replace(',','')
    if int(num) >= 9911:
        return True
    else:
        return False

def rpm_string(stdout):
    fail_packages = re.findall(r'(installed)',stdout)
    return len(fail_packages)

def ls_string(stdout):
    return True if stdout else False

def nginx_check(stdout):
    num = re.findall('\d+', stdout)
    if int(num[0]) >= 4:
        return True
    else:
        return False

def php_page_check(stdout):
    resu = re.findall(r'(test php)', stdout)
    return True if resu else False

def services_check(stdout):
    services_status = []
    # print(stdout)
    s = stdout
    while s.find('Active') != -1:
        index = s.find('Active')
        substr = s[index:index + 17]
        subsubstr = re.search(r'(Active:)(.*)', substr)
        if subsubstr:
            status = re.findall(r'\sactive', subsubstr.group(2))
            if status:
                services_status.append(True)
            else:
                services_status.append(False)
        else:
            return False
        s = s.replace(substr, '',1)
    for status in services_status:
        if not status:
            return False
    return True

def module_check(stdout):
    return True if stdout else False

def mysql_check(stdout):
    resu = re.findall(r'True',stdout)
    return True if resu else False

def python3_check(stdout):
    resu = re.findall(r'python3', stdout)
    return True if resu else False

def ceph_check(stdout):
    resu = re.findall(r'ceph-mon', stdout)
    return True if resu else False

def hosts_initial_check(stdout):
    num = re.findall('\d+', stdout)
    if int(num[0]) == 2:
        return True
    else:
        return False

def hosts_check(stdout):
    num = re.findall('\d+', stdout)
    if int(num[0]) > 2:
        return True
    else:
        return False

def chrony_check(stdout):
    resu = re.findall(r'\^\*', stdout)
    return True if resu else False

def no_check(stdout):
    return True

def mon_number(stdout):
    result = re.findall(r'\d+ mons', stdout)
    subresult = re.findall(r'\d+', result[0])
    return int(subresult[0])

def osd_check(stdout):
    resu = re.findall(r'HEALTH_OK', stdout)
    return True if resu else False

if __name__ == '__main__':
    s='1a111111111a1111111111111111a111111111a'
    s2 = s.replace('a','s')
    print(s2)