from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to string.pdb.text.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.pdb.text
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_string_pdb_text import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, skip_digestion=True)

    return tmp_item

