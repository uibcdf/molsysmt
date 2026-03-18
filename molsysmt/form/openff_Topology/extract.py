from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openff.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):
        from copy import deepcopy
        return deepcopy(item)
    else:
        raise NotImplementedMethodError()
