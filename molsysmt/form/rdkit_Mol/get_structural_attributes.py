import types

from molsysmt._private.argdigest import arg_digest

form = "rdkit.Mol"


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Counting selected RDKit conformers without reading their coordinates.

    Parameters
    ----------
    item : molecular system
        RDKit molecule supplying its ordered conformer inventory.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Conformer positions to count. Repetitions count separately. None and
        'all' count the complete inventory; explicit positions are validated.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        Number of selected conformers, including zero for an empty scope.

    Raises
    ------
    ArgumentError
        If explicit structure indices have invalid types or exceed the conformer axis.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import validate_structure_indices

    count = item.GetNumConformers()
    if structure_indices is None or is_all(structure_indices):
        return count
    indices = validate_structure_indices(
        item,
        structure_indices,
        "molsysmt.form.rdkit_Mol.get_n_structures_from_system",
        count_getter=lambda _: count,
    )
    return len(indices)


# List of functions to be imported
__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
