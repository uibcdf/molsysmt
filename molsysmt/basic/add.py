from molsysmt._private.digestion import digest

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

    from . import get_form, convert, extract, select
    from molsysmt.form import _dict_modules

    if not isinstance(to_molecular_system, (list, tuple)):
        to_molecular_system = [to_molecular_system]

    to_forms = get_form(to_molecular_system)

    for aux_to_item, aux_to_form in zip(to_molecular_system, to_forms):

        aux_item = convert(from_molecular_system, to_form=aux_to_form, selection=selection,
                           structure_indices=structure_indices, syntax=syntax)

        _dict_modules[aux_to_form].add(aux_to_item, aux_item)

    pass

