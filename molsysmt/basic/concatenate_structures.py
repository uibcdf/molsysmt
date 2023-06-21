from molsysmt._private.digestion import digest

@digest()
def concatenate_structures(molecular_systems, selections='all', structure_indices='all', to_form=None):
    """
    Concatenating the structures found in a list of molecular systems.

    The structures found in a list of molecular system are concatenated and returned in a new
    molecular system. Every system must have the same number of atoms. Otherwise the input argument
    ``selections`` needs to be used to select the elements defining the structures to be
    concatenated. In addition, the argument ``structure_indices`` can be used to choose specific
    structures in any of the molecular systems.


    Parameters
    ----------
    molecular_systems : list of molecular systems
        A list of molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        The structures to be concatenated are chosen from these systems.

    selections : list of (tuple, list, numpy.ndarrays, str), or 'all', default 'all'
        Selections of atoms to which this function applies. The default value is 'all' to indicate
        that all entire structures in all systems will be concatenated. If different sets of elements need
        to be specified to extract structures from the list of systems, a list of selections given
        by lists, tuples, numpy arrays of atom indices (0-based
        integers), or strings following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>` must be provided. This former list
        will be applied to the list of molecular systems in the same order.

    structure_indices : list of (tuple, list, numpy.ndarray, 'all'), or 'all', default 'all'
        List of indices of structures (0-based integers) to which this function applies. The
        default value is 'all' to indicate that all structures in all systems will be concatenated.
        If a list of different indices of structures is introduced, they
        will be read and applied to the list of molecular systems in the same order.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the argument
        `selection` (in case it is a string).

    to_form: str or None, default None
        Form of the output molecular system. If no form is indicated, with the default value None, the
        output form will be the same as the first molecular system found in ``molecular_systems``.


    Returns
    -------

    molecular system
        A molecular system with the topology extracted from the first molecular
        system of the list is returned. This molecular system has all the
        structures required by the user by means or the input arguments
        concatenated. The form of this output system can be chosen making use
        of the `to_form` input argument.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions. 

    SyntaxError
        The function raises a SyntaxError in case the syntax argument takes a not supported value. 


    .. versionadded:: 0.1.0

    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.    

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.    


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system

    :func:`molsysmt.basic.append_structures`
        Adding structures from a molecular system to another molecular system.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.basic.convert(demo['alanine dipeptide']['alanine_dipeptide.msmpk'])
    >>> molecular_system_2 = msm.structure.translate(molecular_system_1, translation='[0.1, 0.1, 0.1] nanometers')
    >>> molecular_system_3 = msm.basic.concatenate_structures([molecular_system_1, molecular_system_2])
    >>> msm.basic.get(molecular_system_3, n_structures=True)
    2


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Concatenate structures <Tutorial_Concatenate_structures>`.    

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

