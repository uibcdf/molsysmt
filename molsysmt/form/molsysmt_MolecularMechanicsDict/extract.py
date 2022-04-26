from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'molsysmt.MolecularMechanicsDict')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    raise NotWithThisMolecularSystemError()

