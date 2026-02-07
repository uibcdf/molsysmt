from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='openmm.CharmmCrdFile')
@dep_digest('openmm')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            raise NotImplementedMethodError()
        else:
            tmp_item = item
    else:

        raise NotImplementedMethodError()

    return tmp_item

