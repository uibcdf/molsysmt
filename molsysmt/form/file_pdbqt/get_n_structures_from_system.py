from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the validated PDBQT structure count.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing one supported rigid receptor or ligand.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) to count. Only zero exists in this profile.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    int
        Explicit source count; a supported PDBQT system has one structure.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import structure_count

    return structure_count(item, structure_indices, text=False)
