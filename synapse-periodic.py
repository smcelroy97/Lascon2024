#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:09:35 2020

STDP synapse
Periodic input

@author: matog
"""
import numpy as np
import matplotlib.pyplot as plt

taufac=100
taurec=5
bigu=0.1

numsteps=100
x=np.zeros(numsteps)
y=np.zeros(numsteps)

uu=bigu
rr=0
df=0.01

for ii in range(1,numsteps+1):
    f=df*ii
    dte=1.0/f
    for j in range(numsteps):
#       dte=-np.log(np.random.uniform(0,1))/f
        uu=uu*(1.-bigu)*np.exp(-dte/taufac)+bigu
        xx=np.exp(-dte/taurec)
        rr=rr*(1.-uu)*xx+1.-xx
#        rr=rr*(1.-uu)*xx+(1.-xx)*(1-uu)
    x[ii-1]=f
    y[ii-1]=uu*rr

plt.xlabel('frequency')
plt.ylabel('synaptic strength')
plt.plot(x,y)
plt.show()