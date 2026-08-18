from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='file:structures_yaml')
def to_file_structures_yaml(item, output_filename, skip_digestion=False):
    """
    Converting from file:structures_yaml to file:structures_yaml.

    Parameters
    ----------
    item : file:structures_yaml
        Source item in file:structures_yaml form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:structures_yaml
        Resulting object in file:structures_yaml form.

    .. versionadded:: 1.0.0
    """
    return output_filename if item == output_filename else item
