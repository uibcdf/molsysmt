from molsysmt._private.digestion import digest

@digest()
def append_structures(to_molecular_system, from_molecular_system, selection='all',
        structure_indices='all', syntax='MolSysMT'):
    """
    Adding structures from a molecular system to another molecular system.

    Structures of a molecular system are appended to another molecular system.
    The indices of the structures from the source system
    (`from_molecular_system`) can be chosen by the input argument
    `structure_indices`. The number of atoms of the structures to be appended
    must be equal to the number of atoms of the target system
    (`to_molecular_system`). Otherwise, the input argument `selection` needs to
    be used to specify the atom indices or elements selected from the source
    system which structural attributes will be appended fulfilling this former condition.


    Parameters
    ----------
    to_molecular_system : molecular system
        Target molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Structures from the source molecular system will be appended to this system.

    from_molecular_system : molecular system
        Source molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Strucctures from this system will be appended to the target molecular system.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms over which this method applies. The selection can be
        given by a list, tuple or numpy array of atom indices (0-based
        integers); or by means of a string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) of the source molecular system
        to get the structural attributes of the selected atoms, if any, to be
        appended.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the argument
        `selection` (in case it is a string).


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

    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.basic.convert(demo['alanine dipeptide']['alanine_dipeptide.msmpk'])
    >>> molecular_system_2 = msm.structure.translate(molecular_system_1, translation='[0.1, 0.1, 0.1] nanometers')
    >>> msm.basic.get(molecular_system_1, n_strctures=True)
    1
    >>> msm.basic.append_structures(molecular_system_1, molecular_system_2)
    >>> msm.basic.get(molecular_system_1, n_structures=True)
    2


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Append structures <Tutorial_Append_structures>`.    

    """

    from . import get_form, convert, extract, get
    from molsysmt.form import _dict_modules

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

    pass

