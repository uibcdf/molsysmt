from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.topology.PDBParser to molsysmt.Topology.

    Parameters
    ----------
    item : MDAnalysis.topology.PDBParser
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from MDAnalysis import Universe
    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_Topology import to_molsysmt_Topology as MDAnalysis_Universe_to_molsysmt_Topology

    tmp_item = Universe(item.filename)

    return MDAnalysis_Universe_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)
