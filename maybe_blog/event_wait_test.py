import threading
# event.wait()##阻断线程向下执行 event_obj.set()#释放进程向下执行
def do(event):
    print('start')
    event.wait()##阻断线程向下执行
    print('execute')

event_obj = threading.Event()
for i in range(10):
    t = threading.Thread(target=do, args=(event_obj,))
    t.start()
event_obj.clear()
inp = 0
for _ in range(100):
    print(inp)
    inp += 1
while True:
    if inp == 99:
        event_obj.set()#释放线程向下执行
        break
