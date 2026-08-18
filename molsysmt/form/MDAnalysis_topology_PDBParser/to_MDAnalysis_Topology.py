from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def to_MDAnalysis_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.topology.PDBParser to MDAnalysis.Topology.

    Parameters
    ----------
    item : MDAnalysis.topology.PDBParser
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.Topology
        Converted molecular system representation.
    """

    tmp_item = item.parse()

    if atom_indices != 'all':
        from molsysmt.form.MDAnalysis_Topology.extract import extract as extract_MDAnalysis_Topology
        tmp_item = extract_MDAnalysis_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
