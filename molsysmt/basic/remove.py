from molsysmt._private.digestion import digest
from molsysmt._private.structure_indices import complementary_structure_indices
from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt._private.variables import is_all

@digest()
def remove(molecular_system, selection=None, structure_indices=None, to_form=None, syntax='MolSysMT'):
    """
    Remove atoms or structures from a molecular system.

    This function creates a new molecular system by removing selected atoms and/or specific
    structures (frames) from the input. The selection of elements is done using the `selection`
    argument, while the `structure_indices` argument allows frame-level removal.

    Parameters
    ----------
    molecular_system : molecular system
        A molecular system in any of the :ref:`supported forms <Introduction_Forms>`.

    selection : str, tuple, list, or numpy.ndarray, optional
        Selection of atoms to be removed from the system. Can be provided as a list, tuple, or NumPy
        array of 0-based indices, or as a selection string using one of the
        :ref:`supported syntaxes <Introduction_Selection>`. If `None`, no atoms are removed.

    structure_indices : str, tuple, list, or numpy.ndarray, optional
        Indices of structures (frames) to be removed. If `None`, no structures are removed.

    to_form : str, optional
        If provided, converts the output molecular system to the specified form. Otherwise, the form
        will match the input.

    syntax : str, default 'MolSysMT'
        Syntax used for interpreting the selection string (if `selection` is a string).

    Returns
    -------
    molecular system
        A new molecular system with the selected atoms and/or structures removed.
        The form of the returned system is either specified by `to_form` or inferred from the input.

    Raises
    ------
    NotSupportedFormError
        If the molecular system is provided in an unsupported form.

    ArgumentError
        If the selection or structure_indices are invalid or incompatible with the system.

    Notes
    -----
    The list of supported molecular system forms is described here:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    For selection string syntax, see:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.select`
        Select atoms or structures from a molecular system.

    Examples
    --------
    Remove chains 0 and 1 from a PDB structure:

    >>> import molsysmt as msm
    >>> system = msm.convert('pdb:1B3T')
    >>> msm.get(system, n_chains=True)
    8
    >>> new_system = msm.remove(system, selection='chain_id==0 or chain_id==1')
    >>> msm.get(new_system, n_chains=True)
    6

    .. admonition:: User guide

       For a tutorial on how to use this function, see:
       :ref:`User Guide > Tools > Basic > Remove <Tutorial_Remove>`

    .. versionadded:: 1.0.0
    """

    from . import select, extract, get

    atom_indices_to_be_kept = 'all'
    structure_indices_to_be_kept = 'all'

    if selection is not None:
        atom_indices_to_be_removed = select(molecular_system, selection=selection, syntax=syntax)
        atom_indices_to_be_kept = complementary_atom_indices(molecular_system, atom_indices_to_be_removed)

    if structure_indices is not None:
        if is_all(structure_indices):
            n_structures = get(molecular_system, element='system', n_structures=True)
            structure_indices= list(range(n_structures))
        structure_indices_to_be_kept = complementary_structure_indices(molecular_system, structure_indices)

    tmp_item = extract(molecular_system, selection=atom_indices_to_be_kept,
                       structure_indices=structure_indices_to_be_kept, to_form=to_form, copy_if_all=False)

    if isinstance(tmp_item, (list, tuple)):
        if len(tmp_item) == 1:
            tmp_item = tmp_item[0]

    return tmp_item

