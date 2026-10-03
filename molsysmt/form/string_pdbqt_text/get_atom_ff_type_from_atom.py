from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def get_atom_ff_type_from_atom(item, indices="all", skip_digestion=False):
    """Getting explicit PDBQT atom ff type.

    Parameters
    ----------
    item : str
        Explicit pdbqt_text: string containing one supported PDBQT system.
    indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    numpy.ndarray
        Source-aligned explicit values.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import atom_attribute

    return atom_attribute(item, 'atom_ff_type', indices, text=True)
