from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Topology import is_molsysmt_Topology

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            is_molsysmt_Topology(to_item)
        except:
            raise WrongFormError('molsysmt.Topology')

    raise NotImplementedError

