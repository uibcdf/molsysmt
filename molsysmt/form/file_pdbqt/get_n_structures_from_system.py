from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the validated PDBQT structure count.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing a rigid receptor, ligand or homogeneous MODEL ensemble.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions to count, preserving repetitions; MODEL labels are independent IDs.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    int
        Number of selected source structures, counting repetitions.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import structure_count

    return structure_count(item, structure_indices, text=False)
