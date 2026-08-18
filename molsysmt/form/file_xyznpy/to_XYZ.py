from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest(form='file:xyznpy')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:xyznpy to XYZ.

    Parameters
    ----------
    item : file:xyznpy
        Source item in file:xyznpy form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    XYZ
        Resulting object in XYZ form.

    .. versionadded:: 1.0.0
    """

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

