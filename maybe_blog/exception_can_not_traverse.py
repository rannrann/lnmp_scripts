list=[1,2,3,4]
if 1:
    try:
        raise ValueError
    except Exception as e:
        for i in list:
            print(i)