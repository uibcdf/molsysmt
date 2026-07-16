from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='molsysmt.MolSys')
def to_file_molsys_yaml(
    item, atom_indices='all', structure_indices='all', output_filename=None,
    skip_digestion=False
):
    """Writing MolSys to a YAML molecular system file."""

    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.to_file_molsys_yaml import to_file_molsys_yaml as dict_to_file

    tmp_item = to_molsysmt_MolSysDict(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return dict_to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
