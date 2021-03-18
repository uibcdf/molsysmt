from importlib import import_module
import os

catalog={}
mmtf_translator={}

current_dir = os.path.dirname(os.path.abspath(__file__))
types = [filename.split('.')[0] for filename in os.listdir(current_dir) if filename.endswith('.py')]
types.remove('__init__')

for aux_type in types:

    mod = import_module('molsysmt.elements.entities.'+aux_type)

    for name in mod.name:
        catalog[name]=aux_type
    mmtf_translator.update(mod.mmtf_translator)


del(mod, name, aux_type, types, current_dir)
