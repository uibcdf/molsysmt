from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native import TopologyDict


@dep_digest('yaml')
@arg_digest(form='file:topology_yaml')
def to_molsysmt_TopologyDict(item, skip_digestion=False):
    """Reading a YAML topology file into TopologyDict."""

    import yaml

    with open(item, 'r', encoding='utf-8') as file_handle:
        data = yaml.safe_load(file_handle)

    return TopologyDict(data=data)
