from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='file:xyz')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .get_structural_attributes import _read_xyz

    tmp_item = _read_xyz(item)

    if not is_all(atom_indices):
        atom_indices = np.sort(np.asarray(atom_indices, dtype=int))
        tmp_item = tmp_item[:, atom_indices, :]

    if not is_all(structure_indices):
        tmp_item = tmp_item[structure_indices, :, :]

    tmp_item = tmp_item * puw.unit('nm')
    tmp_item = puw.standardize(tmp_item)

    return tmp_item
