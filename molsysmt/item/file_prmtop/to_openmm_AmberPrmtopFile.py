from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_AmberPrmtopFile(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:prmtop')
        atom_indices = digest_atom_indices(atom_indices)

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

