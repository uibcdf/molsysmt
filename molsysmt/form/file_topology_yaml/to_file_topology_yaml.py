from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest


@dep_digest('yaml')
@arg_digest(form='file:topology_yaml')
def to_file_topology_yaml(item, output_filename, skip_digestion=False):
    """Copying a YAML topology file through TopologyDict serialization."""

    from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
    from molsysmt.form.molsysmt_TopologyDict.to_file_topology_yaml import to_file_topology_yaml as dict_to_file

    tmp_item = to_molsysmt_TopologyDict(item, skip_digestion=True)
    return dict_to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
