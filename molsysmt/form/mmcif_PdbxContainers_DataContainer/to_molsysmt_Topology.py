from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to molsysmt.Topology.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item in mmcif.PdbxContainers.DataContainer form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    get_missing_bonds : object
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item.topology

