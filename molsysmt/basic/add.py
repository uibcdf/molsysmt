from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

__doctest__ = True

@digest()
def add(to_molecular_system, from_molecular_system, selection='all', structure_indices='all',
        keep_ids=True, in_place=True, syntax='MolSysMT', skip_digestion=False):
    """
    Adding elements from one molecular system into another.

    This function adds selected elements from a source molecular system (`from_molecular_system`)
    into a target molecular system (`to_molecular_system`). Both systems must be compatible in
    terms of structure count: if the target system contains structural information (e.g., coordinates),
    the source must either match this number of structures or the user must explicitly provide
    `structure_indices` to specify which structures to use during the addition.

    Parameters
    ----------
    to_molecular_system : molecular system
        The target molecular system, in any of the :ref:`supported forms <Introduction_Forms>`.
        Elements from the source system will be added to this system by default. If `in_place=False`, 
        a copy will be returned instead of modifying this object directly.
    from_molecular_system : molecular system
        The source molecular system, in any of the :ref:`supported forms <Introduction_Forms>`.
        Selected elements from this system will be added to the target system.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atoms to be added, specified as a list/tuple/array of 0-based atom indices,
        or as a string following one of the :ref:`supported selection syntaxes <Introduction_Selection>`.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Indices (0-based) of structures in the source system to use for copying structural attributes
        (e.g., coordinates) of the selected atoms.
    keep_ids : bool, default=True
        Whether to preserve the unique IDs of elements from the source system when adding them
        to the target system.
    in_place : bool, default=True
        If True, modifies `to_molecular_system` in place. If False, returns a new modified copy, leaving
        the original unchanged.
    syntax : str, default='MolSysMT'
        Selection syntax to interpret the `selection` string. See :ref:`Introduction_Selection` for options.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Returns
    -------
    molecular system or None
        If `in_place=True`, returns `None` and modifies `to_molecular_system` directly.
        If `in_place=False`, returns a new molecular system (same form as the input) with the added structures.

    Raises
    ------
    NotSupportedFormError
        If any molecular system is provided in an unsupported form.
    ArgumentError
        If any argument has an invalid or inconsistent value.

    Notes
    -----
    - All forms listed in :ref:`Introduction_Forms` are accepted for both source and target systems.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select` :
        Select elements from a molecular system.
    :func:`molsysmt.basic.merge` :
        Merge multiple molecular systems into one.
    :func:`molsysmt.basic.append_structures` :
        Append structures from one system to another.
    :func:`molsysmt.basic.concatenate_structures` :
        Concatenate multiple systems along the structural dimension.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys_A = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> molsys_B = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'])
    >>> msm.get(molsys_A, n_molecules=True)
    1
    >>> msm.add(molsys_A, molsys_B)
    >>> msm.get(molsys_A, n_molecules=True)
    2

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples: :ref:`Tutorial_Add`.

    .. versionadded:: 1.0.0
    """

    from . import get_form, convert, select, copy
    from molsysmt.form import _dict_modules

    if not in_place:
        to_molecular_system = copy(to_molecular_system)

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    if not isinstance(from_molecular_system, (list, tuple)):
        from_molecular_system = [from_molecular_system]

    from_forms = get_form(from_molecular_system)

    if is_all(selection):
        atom_indices=selection
    else:
        atom_indices=select(from_molecular_system, selection=selection, syntax=syntax)


    for to_item, to_form in zip(to_molecular_system, to_forms):
        for from_item, from_form in zip(from_molecular_system, from_forms):

            if to_form!=from_form:
                aux_from_item = convert(from_item, to_form=to_form, selection=atom_indices, structure_indices=structure_indices)
                aux_atom_indices = 'all'
                aux_structure_indices = 'all'
            else:
                aux_from_item = from_item
                aux_atom_indices = atom_indices
                aux_structure_indices = structure_indices

        add_arguments = {}
        add_function = _dict_modules[to_form].add
        input_arguments = set(inspect.signature(add_function).parameters)

        if 'atom_indices' in input_arguments:
            add_arguments['atom_indices']=aux_atom_indices

        if 'structure_indices' in input_arguments:
            add_arguments['structure_indices']=aux_structure_indices

        add_function(to_item, aux_from_item, keep_ids=keep_ids, **add_arguments)

    if not in_place:
        return to_molecular_system
    else:
        pass

