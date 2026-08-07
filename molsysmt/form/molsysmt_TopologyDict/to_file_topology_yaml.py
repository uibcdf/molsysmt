from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='molsysmt.TopologyDict')
def to_file_topology_yaml(item, output_filename, skip_digestion=False):
    """Writing TopologyDict to a YAML topology file."""

    import yaml

    with open(output_filename, 'w', encoding='utf-8') as file_handle:
        yaml.safe_dump(item.to_dict(copy=True), file_handle, sort_keys=False)

    return output_filename
