from netpyne import specs, sim

netParams = specs.NetParams()
simConfig = specs.SimConfig()

# Create a cell type
# ------------------

netParams.cellParams['pyr'] = {}
netParams.cellParams['pyr']['secs'] = {}

# Add a soma section
netParams.cellParams['pyr']['secs']['soma'] = {}
netParams.cellParams['pyr']['secs']['soma']['geom'] = {
    "diam": 12,
    "L": 12,
    "Ra": 100.0,
    "cm": 1
}

# Add hh mechanism to soma
netParams.cellParams['pyr']['secs']['soma']['mechs'] = {"hh": {
    "gnabar": 0.12,
    "gkbar": 0.036,
    "gl": 0.0003,
    "el": -54.3
}}

# Add a dendrite section
dend = {}
dend['geom'] = {"diam": 1.0,
                "L": 200.0,
                "Ra": 100.0,
                "cm": 1,
                }

# Add pas mechanism to dendrite
dend['mechs'] = {"pas":
                     {"g": 0.001,
                      "e": -70}
                 }

# Connect the dendrite to the soma
dend['topol'] = {"parentSec": "soma",
                 "parentX": 1.0,
                 "childX": 0,
                 }

# Add the dend dictionary to the cell parameters dictionary
netParams.cellParams['pyr']['secs']['dend'] = dend

# Create a population of these cells
# ----------------------------------
netParams.popParams['E'] = {
    "cellType": "pyr",
    "numCells": 40,
}

# Add Exp2Syn synaptic mechanism
# ------------------------------
netParams.synMechParams['exc'] = {
    "mod": "Exp2Syn",
    "tau1": 0.1,
    "tau2": 1.0,
    "e": 0
}

# Define the connectivity
# -----------------------
netParams.connParams['E->E'] = {
    "preConds": {"pop": "E"},
    "postConds": {"pop": "E"},
    "weight": 0.005,
    "probability": 0.1,
    "delay": 5.0,
    "synMech": "exc",
    "sec": "dend",
    "loc": 1.0,
}

# Add a stimulation
# -----------------
netParams.stimSourceParams['IClamp1'] = {
    "type": "IClamp",
    "dur": 5,
    "del": 20,
    "amp": 0.1,
}

# Connect the stimulation
# -----------------------
netParams.stimTargetParams['IClamp1->cell0'] = {
    "source": "IClamp1",
    "conds": {"cellList": [0]},
    "sec": "dend",
    "loc": 1.0,
}

# Set up the simulation configuration
# -----------------------------------

simConfig.filename = "netpyne_tut1"
simConfig.duration = 200.0
simConfig.dt = 0.1

# Record from cell 0
simConfig.recordCells = [0]

# Record the voltage at the soma and the dendrite
simConfig.recordTraces = {
    "V_soma": {
        "sec": "soma",
        "loc": 0.5,
        "var": "v",
    },
    "V_dend": {
        "sec": "dend",
        "loc": 1.0,
        "var": "v",
    }
}

# Record somatic conductances
simConfig.recordTraces['gNa'] = {'sec': 'soma', 'loc': 0.5, 'mech': 'hh', 'var': 'gna'}
simConfig.recordTraces['gK'] = {'sec': 'soma', 'loc': 0.5, 'mech': 'hh', 'var': 'gk'}
simConfig.recordTraces['gL'] = {'sec': 'soma', 'loc': 0.5, 'mech': 'hh', 'var': 'gl'}

# Automatically generate some figures
simConfig.analysis = {
    "plotTraces": {
        "include": [0],
        "saveFig": True,
        "overlay": True,
    },
    "plotRaster": {
        "saveFig": True,
        "marker": "o",
        "markerSize": 50,
    },
    "plotConn": {
        "saveFig": True,
        "feature": "weight",
        "groupBy": "cell",
        # "markerSize": 50,
    },
    "plot2Dnet": {
        "saveFig": True,
    },
}

# Create, simulate, and analyze the model
# ---------------------------------------
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

# Set up the recording for the synaptic current plots
syn_plots = {}
for index, presyn in enumerate(sim.net.allCells[0]['conns']):
    trace_name = 'i_syn_' + str(presyn['preGid'])
    syn_plots[trace_name] = None
    simConfig.recordTraces[trace_name] = {'sec': 'dend', 'loc': 1.0, 'synMech': 'exc', 'var': 'i', 'index': index}

# Create, simulate, and analyze the model
# ---------------------------------------
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

# Extract the data
# ----------------
time = sim.allSimData['t']
v_soma = sim.allSimData['V_soma']['cell_0']
v_dend = sim.allSimData['V_dend']['cell_0']

for syn_plot in syn_plots:
    syn_plots[syn_plot] = sim.allSimData[syn_plot]['cell_0']

# Plot our custom figure
# ----------------------
import matplotlib.pyplot as plt

fig = plt.figure()

plt.subplot(211)
plt.plot(time, v_soma, label='v_soma')
plt.plot(time, v_dend, label='v_dend')
plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('Membrane potential (mV)')

plt.subplot(212)
for syn_plot in syn_plots:
    plt.plot(time, syn_plots[syn_plot], label=syn_plot)
plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('Synaptic current (nA)')

plt.savefig('syn_currents.jpg', dpi=600)