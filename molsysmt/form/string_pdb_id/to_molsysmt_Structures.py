from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_id to molsysmt.Structures.

    Parameters
    ----------
    item : string:pdb_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from molsysmt.form.mmcif_PdbxContainers_DataContainer.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
    from molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_Structures import to_molsysmt_Structures as mmcif_PdbxContainers_DataContainer_to_molsysmt_Structures

    tmp_item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = mmcif_PdbxContainers_DataContainer_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                              structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
