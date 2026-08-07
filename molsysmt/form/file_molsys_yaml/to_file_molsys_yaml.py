from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='file:molsys_yaml')
def to_file_molsys_yaml(item, output_filename, skip_digestion=False):
    """Copying a YAML molecular system file."""

    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.to_file_molsys_yaml import to_file_molsys_yaml as dict_to_file

    tmp_item = to_molsysmt_MolSysDict(item, skip_digestion=True)
    return dict_to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
