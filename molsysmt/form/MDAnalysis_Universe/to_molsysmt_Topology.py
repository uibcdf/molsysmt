from molsysmt._private.argdigest import arg_digest
@arg_digest(form='MDAnalysis.Universe')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.Universe to molsysmt.Topology.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.MDAnalysis_Topology.to_molsysmt_Topology import (
        to_molsysmt_Topology as topology_to_molsysmt_Topology,
    )

    return topology_to_molsysmt_Topology(
        item._topology,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
