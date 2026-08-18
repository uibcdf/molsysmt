from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.topology.PDBParser to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from MDAnalysis import Universe
    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_Topology import to_molsysmt_Topology as MDAnalysis_Universe_to_molsysmt_Topology

    tmp_item = Universe(item.filename)

    return MDAnalysis_Universe_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)
