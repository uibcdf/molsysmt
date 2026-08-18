from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_MDAnalysis_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to MDAnalysis.Topology.

    Parameters
    ----------
    item : file:pdb
        Source item in file:pdb form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Topology
        Resulting object in MDAnalysis.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_MDAnalysis_topology_PDBParser import to_MDAnalysis_topology_PDBParser
    from molsysmt.form.MDAnalysis_topology_PDBParser.to_MDAnalysis_Topology import to_MDAnalysis_Topology as MDAnalysis_topology_PDBParser_to_MDAnalysis_Topology

    tmp_item = to_MDAnalysis_topology_PDBParser(item, skip_digestion=True)
    tmp_item = MDAnalysis_topology_PDBParser_to_MDAnalysis_Topology(tmp_item,
            atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

