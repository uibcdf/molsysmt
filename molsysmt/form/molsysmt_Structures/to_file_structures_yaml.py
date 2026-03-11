from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='molsysmt.Structures')
def to_file_structures_yaml(item, output_filename, atom_indices='all', structure_indices='all', skip_digestion=False):
    """Writing Structures to a declarative YAML structures file."""

    from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
    from molsysmt.form.molsysmt_StructuresDict.to_file_structures_yaml import to_file_structures_yaml as _to_file

    tmp_item = to_molsysmt_StructuresDict(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    return _to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
