from molsysmt._private.digestion import digest

@digest()
def append_structures(to_molecular_system, from_molecular_system, selection='all',
                      structure_indices='all', syntax='MolSysMT', in_place=True,
                      skip_digestion=False):
    """
    Appending structures from one molecular system into another.
    
    This function appends structural information (coordinates, box dimensions, velocities, etc.)
    from a source molecular system (`from_molecular_system`) into a target molecular system
    (`to_molecular_system`). The result is a molecular system with additional structures
    (frames or conformations).
    
    The appended structures must correspond to the same number of atoms as the target system.
    If the number of atoms differs, a selection of atoms from the source system must be
    provided using the `selection` argument. Only the structural attributes of the selected atoms
    will be appended, and they must match the number of atoms in the target system.
    
    By default, the operation modifies the input molecular system in place. This behavior can be
    changed by setting `in_place=False`, in which case a new molecular system is returned.
    
    Parameters
    ----------
    to_molecular_system : molecular system
        Molecular system that will receive the new structures. Must be in one of
        :ref:`the supported forms <Introduction_Forms>`.
    from_molecular_system : molecular system
        Molecular system providing the structures to append. Must be in one of
        :ref:`the supported forms <Introduction_Forms>`.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of atoms from the source system whose structural attributes
        will be appended. Can be a list/array of 0-based atom indices, or a string using
        any of the supported selection syntaxes (:ref:`Introduction_Selection`).
        Only needed when the number of atoms differs between systems.
    structure_indices : int, list, tuple, numpy.ndarray or 'all', default 'all'
        0-based indices of the structures in the source system to append.
    syntax : str, default 'MolSysMT'
        Selection syntax used if `selection` is a string. Must be one of the
        supported syntaxes in :ref:`Introduction_Selection`.
    in_place : bool, default True
        If True, modifies `to_molecular_system` directly. If False, returns a new
        molecular system with the appended structures, leaving the original unmodified.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism. Use with caution.
    
    Returns
    -------
    molecular system or None
        If `in_place=True`, returns `None` and modifies `to_molecular_system` directly.
        If `in_place=False`, returns a new molecular system (same form as the input) with the appended structures.

    Raises
    ------
    NotSupportedFormError
        If either molecular system is not provided in a supported form.
    ArgumentError
        If arguments are inconsistent or conditions are not met, such as mismatched
        atom counts without a proper selection.
    SyntaxError
        If the selection syntax is not recognized.

    Notes
    -----
    - All forms listed in :ref:`Introduction_Forms` are accepted for both source and target systems.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select` :
        Select atoms from a molecular system.
    :func:`molsysmt.basic.concatenate_structures` :
        Concatenate structures from multiple molecular systems into one.
    :func:`molsysmt.basic.add` :
        Adding elements from one molecular system into another.
    :func:`molsysmt.basic.merge` :
        Merge multiple molecular systems into one.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys_A = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    >>> msm.get(molsys_A, n_structures=True)
    1
    >>> msm.append_structures(molsys_A, molsys_B)
    >>> msm.get(molsys_A, n_structures=True)
    2
    
    .. admonition:: Tutorial with more examples
    
       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples: :ref:`Tutorial_Append_structures`.

    .. versionadded:: 1.0.0
    """

    from . import get_form, convert, extract, get, copy
    from molsysmt.form import _dict_modules

    if not in_place:
        to_molecular_system = copy(to_molecular_system)

    _input_was_sequence = isinstance(to_molecular_system, (list, tuple))

    if not _input_was_sequence:
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    coordinates, velocities = get(from_molecular_system, element='atom', selection=selection, syntax=syntax,
                      structure_indices=structure_indices, coordinates=True, velocities=True, skip_digestion=True)

    structure_id, time, box = get(from_molecular_system, element='system', structure_indices=structure_indices,
                                  syntax=syntax, structure_id=True, time=True, box=True, skip_digestion=True)

    if selection != 'all':
        n_sel = coordinates.shape[1]
        n_target_atoms = get(to_molecular_system, element='system', n_atoms=True)
        if n_sel != n_target_atoms:
            raise ValueError(
                f"Selected atoms ({n_sel}) do not match target n_atoms ({n_target_atoms}). "
                "Adjust `selection` or ensure systems have the same number of atoms."
            )

    for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

        _dict_modules[aux_to_form].append_structures(aux_to_item, structure_id=structure_id, time=time, coordinates=coordinates, box=box,
                velocities=velocities)

    if not in_place:
        return to_molecular_system if _input_was_sequence else to_molecular_system[0]
    else:
        pass

