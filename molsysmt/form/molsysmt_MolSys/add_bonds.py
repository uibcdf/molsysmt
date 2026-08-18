from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='molsysmt.MolSys')
def add_bonds(item, bonded_atom_pairs, skip_digestion=False):
    """
    Performing add bonds on form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
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

    item.topology.add_bonds(bonded_atom_pairs, skip_digestion=True)

