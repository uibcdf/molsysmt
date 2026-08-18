from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest
from molsysmt.native import TopologyDict


@dep_digest('yaml')
@arg_digest(form='file:topology_yaml')
def to_molsysmt_TopologyDict(item, skip_digestion=False):
    """
    Converting from file:topology_yaml to molsysmt.TopologyDict.

    Parameters
    ----------
    item : file:topology_yaml
        Source item in file:topology_yaml form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.TopologyDict
        Resulting object in molsysmt.TopologyDict form.

    .. versionadded:: 1.0.0
    """

    import yaml

    with open(item, 'r', encoding='utf-8') as file_handle:
        data = yaml.safe_load(file_handle)

    return TopologyDict(data=data)
