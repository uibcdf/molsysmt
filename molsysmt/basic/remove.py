from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.structure_indices import complementary_structure_indices
from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt._private.variables import is_all

@arg_digest()
def remove(molecular_system, selection=None, structure_indices=None, to_form=None, syntax='MolSysMT',
           skip_digestion=False):
    """
    Removing atoms or structures from a molecular system.

    This function returns a new molecular system after removing the atoms and/or structures
    specified via `selection` and `structure_indices`. If `selection` is `None`, no atoms are
    removed. If `structure_indices` is `None`, no structures are removed. Optionally,
    the resulting system can be returned in a different form with `to_form`.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system provided in any of the :ref:`supported forms <Introduction_Forms>`.
    selection : str, tuple, list or numpy.ndarray, optional
        Atoms to remove, as a 0-based index collection or a selection string parsed according to
        :ref:`Introduction_Selection`. If `'all'`, all atoms are removed. If `None`, no atoms are removed.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', optional
        0-based indices of structures to remove. If `'all'`, all frames are removed.
        If `None`, no structures are removed.
    to_form : str, optional
        Output form of the resulting molecular system. If omitted, the output form matches
        the input system.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

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
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - Removal is implemented by selecting the complementary indices and delegating to
      :func:`molsysmt.basic.extract`, minimizing data copies when possible.

    See Also
    --------
    :func:`molsysmt.select`
        Select atoms or structures from a molecular system.
    :func:`molsysmt.basic.extract` :
        Extract a subset of atoms/structures into a new molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> system = msm.convert('1B3T')
    >>> msm.get(system, n_chains=True)
    8
    >>> new_system = msm.remove(system, selection='chain_id=="A" or chain_id=="B"')
    >>> msm.get(new_system, n_chains=True)
    6

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Remove`.

    .. versionadded:: 1.0.0
    """

    from . import select, extract, get

    atom_indices_to_be_kept = 'all'
    structure_indices_to_be_kept = 'all'

    if selection is not None:
        atom_indices_to_be_removed = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
        atom_indices_to_be_kept = complementary_atom_indices(molecular_system, atom_indices_to_be_removed)

    if structure_indices is not None:
        if is_all(structure_indices):
            n_structures = get(molecular_system, element='system', n_structures=True, skip_digestion=True)
            structure_indices= list(range(n_structures))
        structure_indices_to_be_kept = complementary_structure_indices(molecular_system, structure_indices)

    tmp_item = extract(molecular_system, selection=atom_indices_to_be_kept,
                       structure_indices=structure_indices_to_be_kept, to_form=to_form, copy_if_all=False,
                       skip_digestion=True)

    if isinstance(tmp_item, (list, tuple)):
        if len(tmp_item) == 1:
            tmp_item = tmp_item[0]

    return tmp_item

