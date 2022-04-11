from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'openmm.AmberPrmtopFile')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if (atom_indices is 'all') and (structure_indices is 'all'):

        if copy_if_all:
            raise NotImplementedError()
        else:
            tmp_item = item
    else:

        raise NotImplementedError()

    return tmp_item

