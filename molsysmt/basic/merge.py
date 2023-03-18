from molsysmt._private.digestion import digest

@digest()
def merge(molecular_systems,
          selections='all',
          structure_indices='all',
          syntax='MolSysMT',
          to_form=None,
          ):

    """merge(items=None, selection='all', structure_indices='all', syntax='MolSysMT' to_form=None)

    XXX

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

    from . import convert, extract, get_form
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
    else:
        to_molecular_system = convert(molecular_systems[0], to_form=to_form, selection=selections[0],
                                      structure_indices=structure_indices[0])

    to_form = get_form(to_molecular_system)
    if not isinstance(to_form, (list, tuple)):
        to_molecular_systems = [to_molecular_system]
        to_forms = [to_form]
    else:
        to_molecular_systems = to_molecular_system
        to_forms = to_form

    for aux_to_item, aux_to_form in zip(to_molecular_systems, to_forms):

        for aux_molecular_system, aux_selection, aux_structure_indices in zip(molecular_systems[1:],
            selections[1:], structure_indices[1:]):

            aux_item = convert(aux_molecular_system, to_form=aux_to_form, selection=aux_selection,
                           structure_indices=aux_structure_indices, syntax=syntax)

            _dict_modules[aux_to_form].add(aux_to_item, aux_item)
        
    if len(to_forms)==1:
        return to_molecular_systems[0]
    else:
        return to_molecular_systems

