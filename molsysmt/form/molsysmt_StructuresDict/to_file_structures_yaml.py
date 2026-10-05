from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@dep_digest("yaml")
@arg_digest(form="molsysmt.StructuresDict")
def to_file_structures_yaml(item, output_filename, skip_digestion=False):
    """
    Converting from molsysmt.StructuresDict to file:structures_yaml.


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
    file:structures_yaml
        Resulting object in file:structures_yaml form.

    Raises
    ------
    FormatError
        If a physical field lacks compatible units or sparse alternate-site
        indices, fields or shapes are invalid.

    Notes
    -----
    Writing schema 0.2 with verified PyUnitWizard quantity records, including
    sparse alternate coordinates and B factors. Atom keys are local integer
    indices. The reader retains support for schema 0.1 canonical units.

    Examples
    --------
    >>> import tempfile
    >>> from pathlib import Path
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> molsys = {'coordinates': msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), 'nm')}
    >>> with tempfile.TemporaryDirectory() as directory:
    ...     filename = to_file_structures_yaml(molsys, str(Path(directory) / 'example.yaml'))
    ...     restored = msm.convert(filename, to_form='molsysmt.StructuresDict')
    ...     restored['coordinates'].shape
    (1, 1, 3)

    .. versionadded:: 1.0.0
    """

    import yaml

    from molsysmt.form._structures_yaml import encode_structures

    data = encode_structures(item)

    with open(output_filename, "w", encoding="utf-8") as file_handle:
        yaml.safe_dump(data, file_handle, sort_keys=False)

    return output_filename
