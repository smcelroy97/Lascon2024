import nest
import nest.raster_plot
import pandas as pd
import numpy as np
from pydoc import source_synopsis
import sys
import matplotlib.pyplot as plt

modules = []
for module in sys.modules:
    if module.startswith('matplotlib'):
        modules.append(module)
for module in modules:
    sys.modules.pop(module)
import matplotlib
matplotlib.use("MacOSX")
from    matplotlib  import  pyplot  as plt



connEE = {'rule': 'pairwise_bernoulli', 'p': 0.3,
                  'allow_autapses': False}
connEI = {'rule': 'pairwise_bernoulli', 'p': 0.3,
                  'allow_autapses': False}
connIE = {'rule': 'pairwise_bernoulli', 'p': 0.1,
                  'allow_autapses': False}

synSpecE = {'weight': nest.random.lognormal(mean=1.0, std=0.5), 'delay': 2.0}
synSpecI = {'weight': nest.random.lognormal(mean= -5.0, std= 0.5), 'delay': 0.5}


nest.ResetKernel()
nest.resolution = 0.1

nest.CopyModel("aeif_cond_alpha", "pyr")
nest.CopyModel("aeif_cond_alpha", "in")

Eparams = {
    "V_th": -50.0,  # threshold potential
    "E_L": -65.0,  # membrane resting potential
    "t_ref": 5.0,  # refractory period
    "V_reset": -65.0,  # reset potential
    "C_m": 150.0,  # membrane capacitance
    "Delta_T": 2.0,
    "tau_w": 500.0,
    "a": 4.0,
    "b": 20.0,
    "E_ex": 0.0,
    "E_in": -80.0,
    "tau_syn_ex": 2.0}

# Create Gamma input
# g = nest.Create('ac_generator', params={'amplitude': 100.0, 'frequency': 40.0}) # device 1
g = nest.Create("poisson_generator", {'rate':15})

# Create noise generators (E and I)
noise = nest.Create('poisson_generator', 2,
                    [{'rate': 70000.0}, {'rate': 20000.0}])  # devices 2 and 3

pyr1spk = nest.Create('spike_recorder', params={'label': 'pyr1'}) # device 4
pyr2spk = nest.Create('spike_recorder', params={'label': 'pyr2'}) # device 5
pv1spk = nest.Create('spike_recorder', params={'label': 'pv1'})  # device 6
pv2spk = nest.Create('spike_recorder', params={'label': 'pv2'}) # device 7
s = nest.Create('spike_recorder', params={'label': 's'})



# E Pop:
pyr_1 = nest.Create('pyr', 80)
nest.Connect(pyr_1, pyr1spk)

pyr_2 = nest.Create('pyr', 80)
nest.Connect(pyr_2, pyr2spk)


# I Pop
pv_1 = nest.Create('in', 20)
nest.Connect(pv_1, pv1spk)

pv_2 = nest.Create('in', 20)
nest.Connect(pv_2, pv2spk)


vM = nest.Create('voltmeter')
nest.Connect(vM, pyr_1[0:50])

# Connect Gamma to input layer
nest.Connect(g, pyr_1, syn_spec={'weight': 10.0})
nest.Connect(g, pv_1, syn_spec={'weight':10.0})

pops = [pyr_1, pyr_2, pv_1, pv_2]

# Connect noise to all
for pop in pops:
    # nest.Connect(noise[:1], pop, syn_spec={'weight': 0.01, 'delay': 1.0})
    # nest.Connect(noise[1:], pop, syn_spec={'weight': -0.05, 'delay': 1.0})
    nest.Connect(pop, s)
    print(pop)
    pop.set(Eparams)

# Connect Pops
nest.Connect(pyr_1, pyr_2, conn_spec= connEE, syn_spec=synSpecE)
nest.Connect(pyr_1, pv_2, conn_spec= connEI, syn_spec=synSpecE)
nest.Connect(pv_1, pyr_1, conn_spec=connIE, syn_spec=synSpecI)
nest.Connect(pv_1, pyr_2, conn_spec=connIE,syn_spec=synSpecI)
nest.Connect(pyr_2, pv_1, conn_spec= connEI, syn_spec=synSpecE)
nest.Connect(pyr_2, pyr_1, conn_spec= connEE, syn_spec=synSpecE)
nest.Connect(pv_2, pyr_1, conn_spec=connIE,syn_spec=synSpecI)
nest.Connect(pv_2, pyr_2, conn_spec=connIE,syn_spec=synSpecI)

# nest.Connect(pyr_1, pyr_1, conn_spec=conn_spec_dict, syn_spec=synSpecE)


nest.Simulate(1000)

ev1=pyr1spk.events
ev2=pv1spk.events
ev3=pyr2spk.events
ev4=pv2spk.events
ev5=s.events
nest.raster_plot.from_device(pyr1spk)
nest.raster_plot.from_device(pyr2spk)
nest.raster_plot.from_device(pv1spk)
nest.raster_plot.from_device(pv2spk)
# nest.voltage_trace.from_device(vM)
# nest.raster_plot.from_device(s)
# plt.plot(ev5['times'], ev5['senders'] - min(ev5['senders']), 'o')
# plt.plot(ev4['times'], ev4['senders'] - min(ev4['senders']), 'o')
# plt.ylim([-0.5, 19.5])
# plt.yticks([])
# plt.title('Individual spike trains for each target')
plt.show()



# nest.raster_plot.from_device(pyr1spk, hist=True);

