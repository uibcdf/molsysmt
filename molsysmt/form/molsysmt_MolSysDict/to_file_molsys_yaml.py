from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='molsysmt.MolSysDict')
def to_file_molsys_yaml(item, output_filename, skip_digestion=False):
    """
    Converting from molsysmt.MolSysDict to file:molsys_yaml.


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
    file:molsys_yaml
        Resulting object in file:molsys_yaml form.


    .. versionadded:: 1.0.0
    """

    import yaml

    with open(output_filename, 'w', encoding='utf-8') as file_handle:
        yaml.safe_dump(item.to_dict(copy=True), file_handle, sort_keys=False)

    return output_filename
