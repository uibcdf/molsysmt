from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
    group_indices="all",
):
    """
    Extracting a subset of elements or structures from form string:amino_acids_3.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Sequence positions selected through the generic extraction contract.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original sequence-group positions; selection precedes terminal-cap filtering.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form._sequence_selection import extract as select_groups

    return select_groups(
        item,
        3,
        atom_indices,
        group_indices,
        structure_indices,
        caller="molsysmt.form.string_amino_acids_3.extract",
    )
