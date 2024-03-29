#Run this in your machine before working with the model to install it:

import nest
nest.set_verbosity('M_ERROR')

from pynestml.frontend.pynestml_frontend import generate_nest_target


generate_nest_target(input_path="models/adex_gamma_E.nestml",   # file containing the neuron model definition
                     suffix="_ml",                               # append to model name to avoid clash with existing model
                     module_name="m1module",                     # enumerate modules; name must end in "module"
                     target_path="tgt",                          # path for auxiliary files generated by NESTML
                     install_path=".")                           # location for generated module; must be "." on EBRAINS

nest.Install('m1module')

# This checks if the model is ok:
models_post = set(nest.node_models)
models_post - models_pre

#This checks the parameters of the model:
nest.GetDefaults('adex_gamma_E_ml')

# How to differentiate between neuron types

E = nest.Create('adex_gamma_E_ml', 80)

I = nest.Create('adex_gamma_E_ml', 20, params={'a': 0, 'b':0,'DeltaT': 0.5})