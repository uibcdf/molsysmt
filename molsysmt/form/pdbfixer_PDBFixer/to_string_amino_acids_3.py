from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pdbfixer.PDBFixer to string.amino.acids.3.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.3
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology

    tmp_item  = to_openm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])

    return tmp_item

