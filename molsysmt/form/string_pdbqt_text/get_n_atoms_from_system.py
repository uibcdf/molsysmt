from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the validated PDBQT atom count.

    Parameters
    ----------
    item : str
        Explicit pdbqt_text: string containing a rigid receptor, ligand or homogeneous MODEL ensemble.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    int
        Number of atoms on the invariant molecular axis shared by all models.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt import read

    record = read(item, text=True)
    return len(record["atoms"])
