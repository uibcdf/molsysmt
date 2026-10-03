from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the validated PDBQT atom count.

    Parameters
    ----------
    item : str
        Explicit pdbqt_text: string containing one supported PDBQT system.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    int
        Explicit source count; a supported PDBQT system has one structure.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read

    record = read(item, text=True)
    return len(record["atoms"])
