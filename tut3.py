from netpyne import specs, sim

# should go after importing netpyne
import matplotlib

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.sizeX = 100 # x-dimension (horizontal length) size in um
netParams.sizeY = 500 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100 # z-dimension (horizontal length) size in um

# Custom variables to use with connectivity rules
netParams.propVelocity = 100.0 # propagation velocity (um/ms)
netParams.probLengthConst = 150.0 # length constant for conn probability (um)




#------------------------------------------------------------------------------
## Cell parameters
netParams.cellParams['E'] = {
    'secs': {
        'soma': {
            'geom': {'diam': 18.8, 'L': 18.8, 'Ra': 123.0},
            'mechs': {
                'hh': {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.0003, 'el': -70}
            }
        }
    }
}
netParams.cellParams['I'] = {
    'secs': {
        'soma': {
            'geom': {'diam': 18.8, 'L': 18.8, 'Ra': 123.0},
            'mechs': {
                'hh': {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.0003, 'el': -70}
            }
        }
    }
}





#------------------------------------------------------------------------------
## Population parameters
netParams.popParams['E2'] = {'cellType': 'E', 'numCells': 30, 'yRange': [50,150]}
netParams.popParams['I2'] = {'cellType': 'I', 'numCells': 30, 'yRange': [50,150]}
netParams.popParams['E4'] = {'cellType': 'E', 'numCells': 30, 'yRange': [150,300]}
netParams.popParams['I4'] = {'cellType': 'I', 'numCells': 30, 'yRange': [150,300]}
netParams.popParams['E5'] = {'cellType': 'E', 'numCells': 30, 'ynormRange': [0.6,1.0]}
netParams.popParams['I5'] = {'cellType': 'I', 'numCells': 30, 'ynormRange': [0.6,1.0]}

#------------------------------------------------------------------------------
## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0}  # NMDA synaptic mechanism
netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 'abs(normal(8.5, 1))', 'e': 'uniform(-70, -90)'}  # GABA synaptic mechanism






#------------------------------------------------------------------------------
# Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0.3}
netParams.stimTargetParams['bkg->E'] = {'source': 'bkg', 'conds': {'cellType': ['E']}, 'weight': 0.02, 'sec': 'soma', 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}
netParams.stimTargetParams['bkg->I'] = {'source': 'bkg', 'conds': {'cellType': ['I']}, 'weight': 0.004, 'sec': 'soma', 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}





#------------------------------------------------------------------------------
# Cell connectivity rules
netParams.connParams['E->all'] = {
  'preConds': {'cellType': 'E'},
  'postConds': {'y': [50,500]},  #  E -> all (100-1000 um)
  'probability': 0.1,                  # probability of connection
  'weight': '0.04*post_ynorm',         # synaptic weight
  'delay': 'dist_3D/propVelocity',      # transmission delay (ms)
  'synMech': 'exc'}                     # synaptic mechanism

netParams.connParams['I->E'] = {
  'preConds': {'cellType': 'I'},
  'postConds': {'pop': ['E2','E4','E5']},       #  I -> E
  'probability': '0.3*exp(-dist_3D/probLengthConst)',   # probability of connection
  'weight': 0.01,                                       # synaptic weight
  'delay': 'dist_3D/propVelocity',                      # transmission delay (ms)
  'sec': 'soma',
  'synMech': 'inh'}                                     # synaptic mechanism





#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

# Run parameters
simConfig = specs.SimConfig()       # object of class simConfig to store simulation configuration
simConfig.duration = 1.0*1e3        # Duration of the simulation, in ms
simConfig.hParams['v_init'] = -65   # set v_init to -65 mV
simConfig.dt = 0.1                  # Internal integration timestep to use
simConfig.verbose = False            # Show detailed messages
simConfig.recordStep = 1             # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'tut_03'   # Set file output name




# Recording/plotting parameters
simConfig.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v', 'include': ['E']}}

simConfig.analysis['plot2Dnet'] = {'showFig': True, 'showConns': False}
simConfig.analysis['plotConn'] = {'showFig': True}
simConfig.analysis['plotTraces'] = {'include': [0, 1]}
simConfig.analysis['plotRaster'] = {'orderBy': 'y', 'orderInverse': True, 'showFig': True}   # Plot a raster

sim.createSimulateAnalyze(netParams, simConfig)