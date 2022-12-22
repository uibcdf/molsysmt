from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import pyunitwizard as puw

@digest(form='file:xyznpy')
def to_XYZ(item, atom_indices='all', structure_indices='all', digest=True):

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

