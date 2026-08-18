from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to molsysmt.MolSys.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Converted molecular system representation.
    """

    from molsysmt.form.parmed_Structure.to_molsysmt_MolSys import to_molsysmt_MolSys as parmed_Structure_to_molsysmt_MolSys

    return parmed_Structure_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices, skip_digestion=True)
