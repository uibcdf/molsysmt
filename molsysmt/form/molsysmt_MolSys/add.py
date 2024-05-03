from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(to_form='molsysmt.MolSys', from_form='molsysmt.MolSys')
def add(to_item, from_item, atom_indices='all', structure_indices='all', keep_ids=True, skip_digestion=False):

    to_item.add(from_item, atom_indices=atom_indices, structure_indices=structure_indices, keep_ids=keep_ids,
                skip_digestion=True)

    pass

