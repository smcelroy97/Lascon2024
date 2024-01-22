import numpy as np
import matplotlib.pyplot as plt

N = 1000                                    # Number of neurons
alpha = 0.16                                # Ratio of patterns to number of neurons
P=N*alpha  # P is the number of patterns to store
Phist=P
if P > 100:
    Phist = 100

overlap=np.zeros(int(P))
itmax=500

xi=np.zeros(shape=(N,int(P)))               # instance of one pattern I think
xi=np.random.choice([-1,1],xi.shape)

w=np.matmul(xi,xi.T)/N

for i in range(N):
    w[i,i]=0

for itp in range(Phist):
    s=np.copy(xi[:,itp])
    for it in range(itmax):
        change=False
        for i in range(N):
            hi=np.dot(w[i,:],s)
            if(hi*s[i]<0):
                s[i]=-s[i]
                change=True
        if(change==False):
            break
    print(itp,it)
    overlap[itp]=np.dot(s,xi[:,itp])/N
plt.hist(overlap)
plt.show()