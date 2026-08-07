from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest
from molsysmt.native import MolSysDict


@dep_digest('yaml')
@arg_digest(form='file:molsys_yaml')
def to_molsysmt_MolSysDict(item, skip_digestion=False):
    """Reading a YAML molecular system file into MolSysDict."""

    import yaml

    with open(item, 'r', encoding='utf-8') as file_handle:
        data = yaml.safe_load(file_handle)

    return MolSysDict(data=data)
