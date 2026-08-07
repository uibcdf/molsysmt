from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='molsysmt.MolSysDict')
def to_file_molsys_yaml(item, output_filename, skip_digestion=False):
    """Writing MolSysDict to a YAML file."""

    import yaml

    with open(output_filename, 'w', encoding='utf-8') as file_handle:
        yaml.safe_dump(item.to_dict(copy=True), file_handle, sort_keys=False)

    return output_filename
