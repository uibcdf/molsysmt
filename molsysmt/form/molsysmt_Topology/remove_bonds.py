from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.Topology')
def remove_bonds(item, bond_indices='all', skip_digestion=False):
    """
    Performing remove bonds on form molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item in molsysmt.Topology form.
    bond_indices : object
        Argument bond_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    return item.remove_bonds(bond_indices=bond_indices, skip_digestion=True)
