from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to parmed.Structure.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.Structure
        Converted molecular system representation.
    """

    from molsysmt.form.parmed_Structure.extract import extract as parmed_Structure_extract

    return parmed_Structure_extract(item, atom_indices=atom_indices,
                                    structure_indices=structure_indices,
                                    copy_if_all=copy_if_all, skip_digestion=True)
