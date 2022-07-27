from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'molsysmt.MolSys')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    tmp_item = item.structures.copy()

    return tmp_item

