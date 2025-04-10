from molsysmt._private.digestion import digest

@digest()
def concatenate_structures(molecular_systems, selections='all', structure_indices='all', to_form=None):
    """
    Concatenate structures from a list of molecular systems into a single molecular system.

    The structures found in a list of molecular systems are concatenated and returned in a new 
    molecular system. All systems must have the same number of atoms. If this is not the case, 
    use the argument ``selections`` to specify matching subsets of atoms. Optionally, 
    ``structure_indices`` can be used to select specific structures from each system.

    Parameters
    ----------
    molecular_systems : list of molecular systems
        List of molecular systems in any of the :ref:`supported forms <Introduction_Forms>`.
        Structures to be concatenated are taken from these systems.

    selections : list of (str, tuple, list, ndarray), or 'all', default 'all'
        Atom selections to extract structures from each molecular system. If different selections
        are needed per system, provide a list with the same length as ``molecular_systems``.
        Each element can be a string (parsed with the selected syntax), or a collection of indices.
        See :ref:`selection syntaxes <Introduction_Selection>` for details.

    structure_indices : list of (int, list, tuple, ndarray), or 'all', default 'all'
        Structure indices to include from each system (0-based). If different indices per system
        are required, provide a list with the same length as ``molecular_systems``.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret selection strings. See :ref:`Introduction_Selection` for options.

    to_form : str or None, default None
        Output form of the new molecular system. If None, the form of the first input system is used.

    Returns
    -------
    molecular_system : molecular system
        A new molecular system with all specified structures concatenated. The topology is inherited
        from the first system in ``molecular_systems``. The output format can be controlled with
        ``to_form``.

    Raises
    ------
    NotSupportedFormError
        If any input molecular system has an unsupported form.

    ArgumentError
        If input values are invalid or inconsistent.

    Notes
    -----
    All molecular systems must have a consistent number of atoms across selected elements.
    Use ``selections`` to align atoms across systems as needed.

    See :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>` for 
    supported forms.

    See :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>` for selection options.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.

    :func:`molsysmt.basic.append_structures`
        Append structures from one molecular system to another.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molsys_A = msm.convert(demo['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    >>> molsys_C = msm.concatenate_structures([molsys_A, molsys_B])
    >>> msm.get(molsys_C, n_structures=True)
    2

    .. admonition:: User guide

       For a hands-on tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Concatenate structures <Tutorial_Concatenate_structures>`

    .. versionadded:: 1.0.0
    """

    from . import convert, extract, get, get_form
    from molsysmt.form import _dict_modules

    n_molecular_systems = len(molecular_systems)

    if not isinstance(selections, (list, tuple)):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not isinstance(structure_indices, (list, tuple)):
        structure_indices = [structure_indices for ii in range(n_molecular_systems)]
    elif len(structure_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")

    if to_form is None:
        to_molecular_system = extract(molecular_systems[0], selection=selections[0],
                                      structure_indices=structure_indices[0])
        to_form = get_form(to_molecular_system)
    else:
        to_molecular_system = convert(molecular_systems[0], to_form=to_form, selection=selections[0],
                                      structure_indices=structure_indices[0])

    for aux_molecular_system, aux_selection, aux_structure_indices in zip(molecular_systems[1:], selections[1:], structure_indices[1:]):

        coordinates, velocities = get(aux_molecular_system, element='atom', selection=aux_selection,
                          structure_indices=aux_structure_indices, coordinates=True, velocities=True)
        structure_id, time, box = get(aux_molecular_system, structure_indices=aux_structure_indices, structure_id=True, time=True,
                              box=True)

        _dict_modules[to_form].append_structures(to_molecular_system, structure_id=structure_id, time=time, coordinates=coordinates,
                velocities=velocities, box=box)

    output = to_molecular_system

    return output

