from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

mmtf_translator = {
    'ZINC ION' : 'Zn',
    'CHLORIDE ION' : 'Cl',
    'POTASSIUM ION' : 'K',
    'IODIDE ION' : 'I',
}

def get_name_from_mmtf_name(name):

    return mmtf_translator[name]
