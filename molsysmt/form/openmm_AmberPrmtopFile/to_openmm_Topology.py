from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'openmm.AmberPrmtopFile')
        atom_indices = digest_atom_indices(atom_indices)

    tmp_item = item.topology

    return tmp_item

