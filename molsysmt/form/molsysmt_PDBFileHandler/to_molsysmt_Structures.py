from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):


    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)

    return tmp_item.structures

