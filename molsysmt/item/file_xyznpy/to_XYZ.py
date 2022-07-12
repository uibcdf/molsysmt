from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import puw

def to_XYZ(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:xyznpy')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    with open(item, 'rb') as fff:
        shape = np.load(fff)
        tmp_item = np.load(fff)

    if not is_all(atom_indices):
        tmp_item = tmp_item[:, atom_indices,:]

    if not is_all(structure_indices):
        tmp_item = tmp_item[structure_indices, :, :]

    tmp_item = tmp_item*puw.unit('nm')
    tmp_item = puw.standardize(tmp_item)

    return tmp_item

