from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.Structures')
def to_file_structures_yaml(item, output_filename, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.Structures to file:structures_yaml.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:structures_yaml
        Resulting object in file:structures_yaml form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
    from molsysmt.form.molsysmt_StructuresDict.to_file_structures_yaml import to_file_structures_yaml as _to_file

    tmp_item = to_molsysmt_StructuresDict(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    return _to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
