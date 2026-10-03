from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting a rigid PDBQT subset or retaining a complete source payload.

    Parameters
    ----------
    item : str or pathlib.Path
        Supported PDBQT source.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include. Tree subsets need explicit remapping.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based); only zero exists.
    output_filename : str or pathlib.Path, default=None
        Destination path for a copied or projected file. Required unless a full
        selection explicitly shares the original item with copy_if_all=False.
    copy_if_all : bool, default=True
        Whether a complete selection is copied. False may share the original item.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str or pathlib.Path
        Selected source in the same form.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read
    from molsysmt._private.variables import is_all

    from .to_file_pdbqt import to_file_pdbqt

    if not copy_if_all and is_all(atom_indices) and is_all(structure_indices):
        read(item, text=False)
        return item
    return to_file_pdbqt(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
    )
