from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.MolSys')
def to_file_molsys_yaml(
    item, atom_indices='all', structure_indices='all', output_filename=None,
    skip_digestion=False
):
    """
    Converting from molsysmt.MolSys to file:molsys_yaml.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:molsys_yaml
        Resulting object in file:molsys_yaml form.


    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.to_file_molsys_yaml import to_file_molsys_yaml as dict_to_file

    tmp_item = to_molsysmt_MolSysDict(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return dict_to_file(tmp_item, output_filename=output_filename, skip_digestion=True)
