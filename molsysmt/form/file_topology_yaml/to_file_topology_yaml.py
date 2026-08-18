from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='file:topology_yaml')
def to_file_topology_yaml(item, output_filename, skip_digestion=False):
    """
    Converting from file:topology_yaml to file:topology_yaml.


    Parameters
    ----------
    item : molecular system
        Argument item.
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

    from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
    from molsysmt.form.molsysmt_TopologyDict.to_file_topology_yaml import to_file_topology_yaml as dict_to_file

    tmp_item = to_molsysmt_TopologyDict(item, skip_digestion=True)
    return dict_to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
