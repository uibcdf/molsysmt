from molsysmt._private.digestion import digest
import inspect

@digest()
def add(to_molecular_system, from_molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT'):

    """XXX

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    to_form: str, default='molsysmt.MolSys'
        Any accepted form by MolSysMt for the output object.

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the element
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`
    Notes
    -----

    """

    from . import get_form, convert, select
    from molsysmt.form import _dict_modules

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

        from_form = get_form(from_molecular_system)

        if aux_to_form==from_form:
            aux_item=from_molecular_system
            if is_all(selection):
                aux_atom_indices=selection
            else:
                aux_atom_indices=selection(from_molecular_system, selection=selection, syntax=syntax)
            aux_structure_indices=structure_indices
        else:
            aux_item = convert(from_molecular_system, to_form=aux_to_form, selection=selection,
                           structure_indices=structure_indices, syntax=syntax)
            aux_atom_indices = 'all'
            aux_structure_indices = 'all'

        add_arguments = {}
        add_function = _dict_modules[aux_to_form].add
        input_arguments = set(inspect.signature(function).parameters)

        if 'atom_indices' in input_arguments:
            add_arguments['atom_indices']=atom_indices

        if 'structure_indices' in input_arguments:
            add_arguments['structure_indices']=structure_indices

        add_function(aux_item, **add_arguments)

    pass

