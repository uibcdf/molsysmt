from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
def to_MDAnalysis_topology_PDBParser(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from MDAnalysis.topology.PDBParser to MDAnalysis.topology.PDBParser.

    Parameters
    ----------
    item : MDAnalysis.topology.PDBParser
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.topology.PDBParser
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all,
                   skip_digestion=True)
