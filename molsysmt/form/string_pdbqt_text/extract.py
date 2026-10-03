from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting a rigid PDBQT subset or retaining a complete source payload.

    Parameters
    ----------
    item : str
        Supported PDBQT source.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include. Tree subsets need explicit remapping.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based); only zero exists.
    copy_if_all : bool, default=True
        Whether a complete selection is copied. False may share the original item.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str
        Selected source in the same form.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read
    from molsysmt._private.variables import is_all

    from .to_string_pdbqt_text import to_string_pdbqt_text

    if not copy_if_all and is_all(atom_indices) and is_all(structure_indices):
        read(item, text=True)
        return item
    return to_string_pdbqt_text(
        item, atom_indices=atom_indices, structure_indices=structure_indices
    )
