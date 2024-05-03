from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import pandas as pd
import numpy as np

@digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices=0, get_missing_bonds=True,
                         skip_digestion=False):

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                 get_missing_bonds=get_missing_bonds, skip_digestion=True)

    return tmp_item.topology

