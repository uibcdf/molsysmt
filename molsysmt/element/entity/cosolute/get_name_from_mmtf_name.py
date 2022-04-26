from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

mmtf_translator = {
    'SULFATE ION' : 'sulfate ion',
    'ACETATE ION' : 'acetate ion',
}

def get_name_from_mmtf_name(name):

    return mmtf_translator[name]
