from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from pdbfixer.PDBFixer to openmm.Topology.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    from ..openmm_Topology.extract import extract as extract_openmm_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

