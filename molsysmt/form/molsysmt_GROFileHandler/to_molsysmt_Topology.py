from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.GROFileHandler')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                         skip_digestion=False):

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                 get_missing_bonds=get_missing_bonds, skip_digestion=True)

    return tmp_item.topology

