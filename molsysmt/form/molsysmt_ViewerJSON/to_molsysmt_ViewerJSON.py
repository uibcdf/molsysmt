from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.ViewerJSON")
def to_molsysmt_ViewerJSON(
    item, skip_digestion=False, *, atom_indices="all", structure_indices="all"
):
    """
    Converting from molsysmt.ViewerJSON to molsysmt.ViewerJSON.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Unique atom indices (0-based) in the requested order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) in the requested order, including repetitions.

    Returns
    -------
    molsysmt.ViewerJSON
        Independent graphics payload with selected atoms, remapped bonds and
        structures in their requested order. Coordinates and boxes remain in nm;
        time remains in ps.

    Raises
    ------
    ArgumentError
        If an index is out of range or atom indices repeat.
    FormatError
        If selected graphics columns or endpoint encodings are inconsistent.

    Examples
    --------
    >>> from molsysmt.native import ViewerJSON
    >>> payload = ViewerJSON(data={"atoms": {"atom_id": ["A", "B"]}})
    >>> to_molsysmt_ViewerJSON(payload, atom_indices=[1]).data["atoms"]["atom_id"]
    ['B']

    .. versionadded:: 1.0.0
    """
    from .extract import extract

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
