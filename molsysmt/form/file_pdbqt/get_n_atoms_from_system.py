from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the validated PDBQT atom count.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing one supported rigid receptor or ligand.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    int
        Explicit source count; a supported PDBQT system has one structure.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read

    record = read(item, text=False)
    return len(record["atoms"])
