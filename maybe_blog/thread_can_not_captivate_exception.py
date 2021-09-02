import threading
def add(a,b):
    if int(b) == 0:
        raise ValueError("wrong")
    result = int(a)/int(b)

def add2(a,b):
    try:
        result = int(a)/int(b)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # 不可以
    # try:
    #     th = threading.Thread(target=add, args=('1','0',))
    #     th.start()
    # except Exception as e:
    #     print(e)

    #可以
    for i in range(3):
        th = threading.Thread(target=add2, args=('1','0',))
        th.start()
