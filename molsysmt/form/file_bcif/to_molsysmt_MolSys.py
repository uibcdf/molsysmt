from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:bcif to molsysmt.MolSys.

    Parameters
    ----------
    item : file:bcif
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Converted molecular system representation.
    """

    from .to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
    from molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys import to_molsysmt_MolSys as mmcif_PdbxContainers_DataContainer_to_molsysmt_MolSys

    tmp_item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = mmcif_PdbxContainers_DataContainer_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                   structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

