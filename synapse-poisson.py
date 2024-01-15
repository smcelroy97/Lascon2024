#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:09:35 2020

STDP synapse
Poisson input


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


nprom=100

for j in range(nprom):
    uu=bigu
    rr=0.0
    df=0.01

    for ii in range(1,numsteps):
        f=df*ii
        for j in range(numsteps):
            dte=-np.log(np.random.uniform(0,1))/f
            uu=uu*(1.-bigu)*np.exp(-dte/taufac)+bigu
            xx=np.exp(-dte/taurec)
            rr=rr*(1.-uu)*xx+1.-xx
        x[ii]=f
        y[ii]=y[ii]+uu*rr

y=y/nprom

plt.xlabel('frequency')
plt.ylabel('synaptic strength')
plt.plot(x,y)