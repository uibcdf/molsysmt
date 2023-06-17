from molsysmt._private.digestion import digest
import numpy as np
from pandas import DataFrame as df


@digest()
def get_label(molecular_system,
         element='system',
         selection='all',
         syntax='MolSysMT',
         output_type='dataframe',
         ):
    """info(item, element='system', indices=None, selection='all', syntax='MolSysMT')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    molecular_system: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    element: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of elementted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).


    selection: str, list, tuple or np.ndarray, default='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT.

    syntax: str, default='MolSysMT'
       Selection syntax used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolSysMt in section 'Selection'.

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

    from . import get_form, get, convert, select
    from molsysmt.element import elements_to_string
    from molsysmt.form import _piped_forms_in_info, _dict_modules

    form = get_form(molecular_system)

    if isinstance(form, (list, tuple)):
        attributes_filter = _dict_modules[form[0]].attributes.copy()
        for aux_form in form[1:]:
            for aux_attribute, aux_bool in _dict_modules[aux_form].attributes.items():
                if aux_bool:
                    attributes_filter[aux_attribute]=True
    else:
        attributes_filter = _dict_modules[form].attributes

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    aux_molecular_system = []
    for ii in molecular_system:
        form_in = get_form(ii)
        if form_in in _piped_forms_in_info:
            jj = convert(ii, to_form='molsysmt.MolSys')
            aux_molecular_system.append(jj)
        else:
            aux_molecular_system.append(ii)
    molecular_system = aux_molecular_system

    if output_type == 'short_string':

        string = elements_to_string(molecular_system, selection=selection, element=element)

        if len(string) == 1:
            return string[0]
        else:
            return string

    elif output_type == 'long_string':

        if element == 'atom':

            group_indices, chain_indices, molecule_indices = get(molecular_system, element=element,
                                                                 selection=selection,
                                                                 group_index=True, chain_index=True,
                                                                 molecule_index=True)

            atom_string = elements_to_string(molecular_system, selection=selection, element=element)
            group_string = elements_to_string(molecular_system, selection=group_indices, element='group')
            chain_string = elements_to_string(molecular_system, selection=chain_indices, element='chain')
            molecule_string = elements_to_string(molecular_system, selection=molecule_indices, element='molecule')

            string = []

            for list_strings in zip(atom_string, group_string, chain_string,
                                    molecule_string):
                string.append('/'.join(list_strings))

            if len(string) == 1:
                string = string[0]

        elif element == 'group':

            chain_indices, molecule_indices = get(molecular_system, element=element,
                    selection=selection, chain_index=True, molecule_index=True)

            group_string = elements_to_string(molecular_system, selection=selection, element=element)
            chain_string = elements_to_string(molecular_system, selection=chain_indices, element='chain')
            molecule_string = elements_to_string(molecular_system, selection=molecule_indices, element='molecule')

            string = []

            for list_strings in zip(group_string, chain_string,
                                    molecule_string):
                string.append('/'.join(list_strings))

            if len(string) == 1:
                string = string[0]

        elif element == 'component':

            chain_indices, molecule_indices = get(molecular_system, element=element, selection=selection, chain_index=True,
                                                  molecule_index=True)

            component_string = elements_to_string(molecular_system, selection=selection, element=element)
            chain_string = elements_to_string(molecular_system, selection=chain_indices, element='chain')
            molecule_string = elements_to_string(molecular_system, selection=molecule_indices, element='molecule')

            string = []

            for list_strings in zip(component_string, chain_string, molecule_string):
                string.append('/'.join(list_strings))

            if len(string) == 1:
                string = string[0]

        elif element == 'chain':

            chain_string = elements_to_string(molecular_system, selection=selection, element=element)
            string = chain_string

            if len(string) == 1:
                string = string[0]

        elif element == 'molecule':

            molecule_string = elements_to_string(molecular_system, selection=selection, element=element)
            string = molecule_string

            if len(string) == 1:
                string = string[0]

        elif element == 'entity':

            entity_string = elements_to_string(molecular_system, selection=selection, element=element)
            string = entity_string

            if len(string) == 1:
                string = string[0]

        else:

            raise NotImplementedError

        return string

    else:

        raise ValueError()

