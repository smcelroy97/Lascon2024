# Deterministic

import numpy as np

N = 1000                                    # Number of neurons
alpha = 0.2                                 # Ratio of patterns to number of neurons
P=N*alpha                                   # P is the number of patterns to store

itmax=500

xi=np.zeros(shape=(N,int(P)))               # instance of one pattern I think
xi=np.random.choice([-1,1],xi.shape)

w=np.matmul(xi,xi.T)/N

for i in range(N):
    w[i,i]=0

for itp in range(int(P)):
    s=np.copy(xi[:,itp])
    for it in range(itmax):
        snew=np.sign(np.matmul(w,s))
        if np.sum((s-snew)**2) == 0:
            break
        s=np.copy(snew)
    print(itp,it)