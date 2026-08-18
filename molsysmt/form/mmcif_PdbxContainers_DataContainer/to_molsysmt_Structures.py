from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to molsysmt.Structures.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item in mmcif.PdbxContainers.DataContainer form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)

    return tmp_item.structures

