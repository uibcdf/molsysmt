from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Context(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'openmm.Simulation')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    tmp_item = item.context

    return tmp_item

