import numpy as np

x1 = [3, 4, 5]
x1Arry=np.array(x1)
# print(type(x1Arry))
# print(x1Arry * 50)

tmp = [[3, 5, 5, 2, 9],
       [2, 3, 4, 2, 3]]

tmpA=np.array(tmp)
tmpA[:,1]=0
# print(tmpA)
print(tmpA, tmpA.sum(axis=1), tmpA.sum(axis=0))