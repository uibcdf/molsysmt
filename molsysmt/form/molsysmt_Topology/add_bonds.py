from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='molsysmt.Topology')
def add_bonds(item, bonded_atom_pairs, skip_digestion=False):
    """
    Performing add bonds on form molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item in molsysmt.Topology form.
    bonded_atom_pairs : object
        Argument bonded_atom_pairs.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    item.add_bonds(bonded_atom_pairs, skip_digestion=True)

