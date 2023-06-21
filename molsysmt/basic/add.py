from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

@digest()
def add(to_molecular_system, from_molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT'):
    """
    Adding elements of a molecular system into another molecular system.

    Elements of a molecular system are added to another molecular system. If
    the target system (`to_molecular_system`) has structures, the source system
    (`from_molecular_system`) must have the same number of structures.
    Otherwise, the input argument `structure_indices` needs to be used to
    specify the indices to extract the structural attributes of the elements to
    be added.


    Parameters
    ----------
    to_molecular_system : molecular system
        Target molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Elements from the source molecular system will be added to this system.

    from_molecular_system : molecular system
        Source molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Elements from this system will be added to the target molecular system.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms to which this method applies. The selection can be
        given by a list, tuple or numpy array of atom indices (0-based
        integers); or by means of a string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) of the source molecular system
        to get the structural attributes of the selected atoms, if any, to be
        added.

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

    :func:`molsysmt.basic.merge`
        Merging the elements of different molecular systems.

    :func:`molsysmt.basic.append_structures`
        Adding structures from a molecular system to another molecular system.

    :func:`molsysmt.basic.concatenate_structures`
        Concatenating the structures found in a list of molecular systems.



    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.basic.convert(demo['alanine dipeptide']['alanine_dipeptide.msmpk'])
    >>> molecular_system_2 = msm.basic.convert(demo['valine dipeptide']['valine_dipeptide.msmpk'])
    >>> msm.basic.get(molecular_system_1, n_molecules=True)
    1
    >>> msm.basic.add(molecular_system_1, molecular_system_2)
    >>> msm.basic.get(molecular_system_1, n_molecules=True)
    2


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Add <Tutorial_Add>`.    

    """

    from . import get_form, convert, select
    from molsysmt.form import _dict_modules

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    if not isinstance(from_molecular_system, (list, tuple)):
        from_molecular_system = [from_molecular_system]

    from_forms = get_form(from_molecular_system)

    if is_all(selection):
        atom_indices=selection
    else:
        atom_indices=selection(from_molecular_system, selection=selection, syntax=syntax)


    for to_item, to_form in zip(to_molecular_system, to_forms):
        for from_item, from_form in zip(from_molecular_system, from_forms):

            if to_form!=from_form:
                aux_from_item = convert(aux_from_item, to_form=aux_to_form, selection=atom_indices, structure_indices=structure_indices)
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

        add_function(to_item, aux_from_item, **add_arguments)

    pass

