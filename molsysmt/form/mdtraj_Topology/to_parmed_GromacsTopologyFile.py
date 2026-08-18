from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Topology to parmed.GromacsTopologyFile.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.GromacsTopologyFile
        Converted molecular system representation.
    """

    from molsysmt.form.parmed_Structure.to_parmed_Structure import to_parmed_Structure
    from molsysmt.form.parmed_Structure.to_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile as parmed_Structure_to_parmed_GromacsTopologyFile

    tmp_item = to_parmed_Structure(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = parmed_Structure_to_parmed_GromacsTopologyFile(tmp_item, skip_digestion=True)

    return tmp_item

