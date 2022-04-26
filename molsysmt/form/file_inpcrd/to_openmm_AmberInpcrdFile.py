from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_AmberInpcrdFile(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:inpcrd')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)

    return tmp_item

