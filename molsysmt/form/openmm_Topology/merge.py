from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_openmm_Topology(item_1)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            is_openmm_Topology(item_2)
        except:
            raise WrongFormError('openmm.Topology')

    raise NotImplementedMethodError()

