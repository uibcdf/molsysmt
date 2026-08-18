from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='molsysmt.TopologyDict')
def to_file_topology_yaml(item, output_filename, skip_digestion=False):
    """
    Converting from molsysmt.TopologyDict to file:topology_yaml.

    Parameters
    ----------
    item : molsysmt.TopologyDict
        Source item in molsysmt.TopologyDict form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:topology_yaml
        Resulting object in file:topology_yaml form.

    .. versionadded:: 1.0.0
    """

    import yaml

    with open(output_filename, 'w', encoding='utf-8') as file_handle:
        yaml.safe_dump(item.to_dict(copy=True), file_handle, sort_keys=False)

    return output_filename
