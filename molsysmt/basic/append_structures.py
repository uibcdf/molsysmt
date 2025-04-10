from molsysmt._private.digestion import digest

@digest()
def append_structures(to_molecular_system, from_molecular_system, selection='all',
                      structure_indices='all', syntax='MolSysMT', in_place=True,
                      skip_digestion=False):
    """
    Append structures from one molecular system into another.

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
        will be appended. Can be a list/array of atom indices, or a string using
        any of the supported selection syntaxes 
        (:ref:`Introduction_Selection`). Only needed when the number of atoms 
        differs between systems.

    structure_indices : int, list, tuple, numpy.ndarray or 'all', default 'all'
        Indices (0-based) of the structures in the source system to append.

    in_place : bool, default True
        If True, modifies `to_molecular_system` directly. If False, returns a new
        molecular system with the appended structures, leaving the original unmodified.

    syntax : str, default 'MolSysMT'
        Selection syntax used if `selection` is a string. Must be one of the
        supported syntaxes in :ref:`Introduction_Selection`.

    in_place : bool, default True
        If True, modifies `to_molecular_system` directly. If False, returns a new
        molecular system with the appended structures, leaving the original unmodified.

    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Raises
    ------
    NotSupportedFormError
        If either molecular system is not provided in a supported form.

    ArgumentError
        If arguments are inconsistent or conditions are not met, such as mismatched
        atom counts without a proper selection.

    SyntaxError
        If the selection syntax is not recognized.

    Returns
    -------
    molecular system or None
        If `in_place=True`, returns `None` and modifies `to_molecular_system` directly.
        If `in_place=False`, returns a new molecular system with the appended structures.

    Notes
    -----
    - All forms listed in :ref:`Introduction_Forms` are accepted.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - Use this function to extend a molecular system with additional structures
      (e.g., when combining simulations or generating trajectories).

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.    

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.    

    See Also
    --------
    :func:`molsysmt.basic.concatenate_structures`
        Concatenates structures from multiple molecular systems into one.
    
    :func:`molsysmt.basic.select`
        Selects atoms or elements from a molecular system.

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

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Append structures <Tutorial_Append_structures>`.

    .. versionadded:: 1.0.0

    """

    from . import get_form, convert, extract, get, copy
    from molsysmt.form import _dict_modules

    if not in_place:
        to_molecular_system = copy(to_molecular_system)

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    coordinates, velocities = get(from_molecular_system, element='atom', selection=selection,
                      structure_indices=structure_indices, coordinates=True, velocities=True)

    structure_id, time, box = get(from_molecular_system, element='system', structure_indices=structure_indices,
                          structure_id=True, time=True, box=True)

    for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

        _dict_modules[aux_to_form].append_structures(aux_to_item, structure_id=structure_id, time=time, coordinates=coordinates, box=box,
                velocities=velocities)

    if not in_place:
        return to_molecular_system
    else:
        pass

