from time import sleep
import threading

def main():
    ins=0
    while 1==1:
        sleep(2)
        txf=threading.Thread(target=fyy,args=(ins,))
        txf.start()
        ins=ins+1
        print('ins=' + str(ins))

def ooo(p):
    ff=[]
    dict={'b':'sss'}

    ff.append(p)
    ff.append('b')
    ff[1]=('k')
    print(tuple(ff))
    print(dict)


    dict0={}
    dict0=dict0.fromkeys(tuple(ff), 'xs')
    dict.update(dict0)

    #dict['c']='21'

    #dict = dict.fromkeys(tuple(ff), 10)

    print(dict)

    #print(ff[1])
    #print(len(ff))
def fyy(ins):
    tt = []
    for i in range(2):
        ii=i
        print(len(tt))
        tt.append(threading.Thread(target=ooo, args=('p',)))
        tt[ii].start()



if __name__ == "__main__":
    main()