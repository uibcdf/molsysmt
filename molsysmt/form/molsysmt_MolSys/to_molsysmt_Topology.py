from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    return item.topology.extract(atom_indices=atom_indices, skip_digestion=True)

