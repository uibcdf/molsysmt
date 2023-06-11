from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

@digest()
def add(to_molecular_system, from_molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT'):

    """Adding elements of a molecular system into another molecular system.

    Elements of a molecular system are added to another molecular system. If the target system
    (`to_molecular_system`) has structures, the source system (`from_molecular_system`) must have
    the same number of structures. Otherwise, the input argument `structure_indices` needs to be
    used to specify the indices to extract the structural attributes of the elements to be added.

    Parameters
    ----------

    to_molecular_system: molecular system
        Target molecular system in any of the supported forms (See :ref:`Add in User Guide 
        <UserGuide_Tools_Basic_Add>`). Elements from the source
        molecular system will be added to this system.

    from_molecular_system: molecular system
        Source molecular system in any of the supported forms (See: XXX). Elements from this system
        will be added to the target molecular system.



    to_form: str, default='molsysmt.MolSys'
        Any accepted form by MolSysMt for the output object.

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Raises
    ------

    Errors raised by the function

    See Also
    --------

    :ref:`User Guide>Tools>Basic>Add <UserGuide_Tools_Basic_Add>`
        Add tutorial in the User Guide.

    :func:`molsysmt.basic.select`
        Selection function.

    Notes
    -----

    .. versionadded:: 0.1.0

    A tutorial on how to work with this function can be found in the documentation section 
    :ref:`User Guide>Tools>Basic>Add <UserGuide_Tools_Basic_Add>`.    

    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.convert(demo['alanine dipeptide']['alanine_dipeptide.msmpk'])
    >>> molecular_system_2 = msm.convert(demo['valine dipeptide']['valine_dipeptide.msmpk'])
    >>> msm.get(molecular_system_1, n_molecules=True)
    1
    >>> msm.add(molecular_system_1, molecular_system_2)
    >>> msm.get(molecular_system_1, n_molecules=True)
    2
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

