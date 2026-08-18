from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):
    """
    Converting from string:alphafold_id to molsysmt.Topology.

    Parameters
    ----------
    item : string:alphafold_id
        Source item in string:alphafold_id form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    get_missing_bonds : object
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """


    from molsysmt.form.string_alphafold_id.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
    from molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_Topology import to_molsysmt_Topology as mmcif_PdbxContainers_DataContainer_to_molsysmt_Topology

    tmp_item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = mmcif_PdbxContainers_DataContainer_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
                                                                       get_missing_bonds=get_missing_bonds,
                                                                       skip_digestion=True)

    return tmp_item

