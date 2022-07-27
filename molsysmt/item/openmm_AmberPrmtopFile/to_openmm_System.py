from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_System(item, atom_indices='all'):

    if check:

        digest_item(item, 'openmm.AmberPrmtopFile')
        atom_indices = digest_atom_indices(atom_indices)

    tmp_item = item.createSystem()

    return tmp_item

