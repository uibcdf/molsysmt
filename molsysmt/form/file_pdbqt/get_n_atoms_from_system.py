from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the validated PDBQT atom count.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing a rigid receptor, ligand or homogeneous MODEL ensemble.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    int
        Number of atoms on the invariant molecular axis shared by all models.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read

    record = read(item, text=False)
    return len(record["atoms"])
