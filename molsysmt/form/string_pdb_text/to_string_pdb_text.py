from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from string:pdb_text to string:pdb_text.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.


    .. versionadded:: 1.0.0
    """

    from .extract import extract

    # An identity converter is the one place a wrong item cannot be inferred from what
    # it is asked to do, and internal two-step conversions reach it with
    # skip_digestion=True, which turns off the form check that would have caught it.
    # That combination is how `uibcdf/molsysmt#180` stayed hidden for eleven days: seven
    # adapters imported this function instead of their own, and the failure surfaced as
    # `NotImplementedError: Widgets cannot be copied` from inside `copy()`.
    if not isinstance(item, str):
        from molsysmt._private.smonitor import NotSupportedFormError
        raise NotSupportedFormError(
            form=type(item).__name__,
            caller='molsysmt.form.string_pdb_text.to_string_pdb_text',
            message=(
                f"string:pdb_text's own converter received a {type(item).__name__}. "
                "This usually means an adapter imported "
                "'molsysmt.form.string_pdb_text.to_string_pdb_text' instead of its own "
                "'from .to_string_pdb_text import to_string_pdb_text'."
            ),
        )

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

