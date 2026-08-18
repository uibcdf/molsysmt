from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest
from molsysmt.native import MolSysDict


@dep_digest('yaml')
@arg_digest(form='file:molsys_yaml')
def to_molsysmt_MolSysDict(item, skip_digestion=False):
    """
    Converting from file:molsys_yaml to molsysmt.MolSysDict.

    Parameters
    ----------
    item : file:molsys_yaml
        Source item in file:molsys_yaml form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysDict
        Resulting object in molsysmt.MolSysDict form.

    .. versionadded:: 1.0.0
    """

    import yaml

    with open(item, 'r', encoding='utf-8') as file_handle:
        data = yaml.safe_load(file_handle)

    return MolSysDict(data=data)
