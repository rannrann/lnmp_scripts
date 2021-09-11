class A:
    sum=0

class B(A):
    def __init__(self):
        print(A.sum)

b=B()