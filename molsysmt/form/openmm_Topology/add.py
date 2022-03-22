from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            is_openmm_Topology(to_item)
        except:
            raise WrongFormError('openmm.Topology')

    raise NotImplementedMethodError()
    pass

