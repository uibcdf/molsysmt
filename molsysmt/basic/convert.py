from molsysmt._private.exceptions import NotImplementedConversionError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

@digest()
def convert(molecular_system,
            to_form='molsysmt.MolSys',
            selection='all',
            structure_indices='all',
            syntax='MolSysMT',
            **kwargs):
    """convert(item, to_form='molsysmt.MolSys', selection='all', structure_indices='all', syntax='MolSysMT', **kwargs)

    Convert an input form of a molecular system into other form.

    A molecular model in a given accepted form can be converted into any other supported form
    by MolSysMt. The list of supported forms can be found in the section 'XXX'.

    Parameters
    ----------

    molecular_system: molecular model
        Molecular model in any supported form by MolSysMT (see: XXX).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    to_form: str, default='molsysmt.MolSys'
        The output object will take the form specified here. This form supported form by MolSysMt
        for the output object.

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------

       item: molecular model

       A new object is returned with the form specified by the argument `to_form`.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.basic.select`

    Notes
    -----

    """

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt._private import _multiple_conversion_shortcuts
    from molsysmt.basic import has_attribute

    tmp_item = None

    from_form = get_form(molecular_system)

    if to_form is None:
        to_form = from_form

    # If to_form is a list, covert is invoked iteratively

    if isinstance(to_form, (list, tuple)):
        tmp_item=[]
        for item_out in to_form:
            tmp_item.append(
                convert(molecular_system, to_form=item_out, selection=selection, structure_indices=structure_indices,
                        syntax=syntax))
        return tmp_item

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)


    # If one to one

    if not isinstance(from_form, (list, tuple)):

        if from_form == to_form:

            function = _dict_modules[from_form].extract

            input_arguments = set(inspect.signature(function).parameters)

            if structure_indices in input_arguments:
                conversion_arguments['structure_indices']=structure_indices

            for element, element_index in _element_index.items():
                if _element_indices[element] in input_arguments:
                    if not is_all(selection):
                        conversion_arguments[_element_indices[element]] = select(molecular_system, element=element, selection=selection, syntax=syntax)
                    else:
                        conversion_arguments[_element_indices[element]] = 'all'
                    break

            conversion_arguments['copy_if_all'] =  True

            tmp_item = function(molecular_system, **conversion_arguments, **kwargs) 

        elif from_form in _dict_modules:

            if to_form in _dict_modules[from_form]._convert_to:

                function = _dict_modules[from_form]._convert_to[to_form]

                input_arguments = set(inspect.signature(function).parameters)

                if structure_indices in input_arguments:
                    conversion_arguments['structure_indices']=structure_indices

                for element, element_index in _element_index.items():
                    if _element_indices[element] in input_arguments:
                        if not is_all(selection):
                            conversion_arguments[_element_indices[element]] = select(molecular_system, element=element, selection=selection, syntax=syntax)
                        else:
                            conversion_arguments[_element_indices[element]] = 'all'
                        break

                tmp_item = function(molecular_system, **conversion_arguments, **kwargs)

            elif ('molsysmt.MolSys' in _dict_modules[from_form]._convert_to) and (to_form in _dict_modules['molsysmt.MolSys']._convert_to):

                function = _dict_modules[from_form]._convert_to['molsysmt.MolSys']

                input_arguments = set(inspect.signature(function).parameters)

                if structure_indices in input_arguments:
                    conversion_arguments['structure_indices']=structure_indices

                for element, element_index in _element_index.items():
                    if _element_indices[element] in input_arguments:
                        if not is_all(selection):
                            conversion_arguments[_element_indices[element]] = select(molecular_system, element=element, selection=selection, syntax=syntax)
                        else:
                            conversion_arguments[_element_indices[element]] = 'all'
                        break

                tmp_item = function(molecular_system, **conversion_arguments, **kwargs)
                tmp_item = _dict_modules['molsysmt.MolSys']._convert_to[to_form](tmp_item)
        
    # If multiple to one

    else:

        from_forms = from_form
        n_items = len(from_forms)

        # conversions in private shortcuts
        sorted_forms = tuple(sorted(from_forms))

        if sorted_forms in _multiple_conversion_shortcuts:

            if to_form in _multiple_conversion_shortcuts[sorted_forms]:

                function = _multiple_conversion_shortcuts[sorted_forms][to_form]

                input_arguments = set(inspect.signature(function).parameters)

                if structure_indices in input_arguments:
                    conversion_arguments['structure_indices']=structure_indices

                for element, element_index in _element_index.items():
                    if _element_indices[element] in input_arguments:
                        if not is_all(selection):
                            conversion_arguments[_element_indices[element]] = select(molecular_system, element=element, selection=selection, syntax=syntax)
                        else:
                            conversion_arguments[_element_indices[element]] = 'all'
                        break

                tmp_item = function(molecular_system, **conversion_arguments, **kwargs)

            elif ('molsysmt.MolSys' in _multiple_conversion_shortcuts[sorted_forms]) and (to_form in _dict_modules['molsysmt.MolSys']._convert_to):

                tmp_item = _multiple_conversion_shortcuts[sorted_forms]['molsysmt.MolSys'](molecular_system, **conversion_arguments, **kwargs)
                tmp_item = _dict_modules['molsysmt.MolSys']._convert_to[to_form](tmp_item)

        #### Checking attributes sets for straight and indirect conversion

        if tmp_item is None:

            to_attributes = set([ii for ii,jj in _dict_modules[to_form].attributes.items() if jj])
            from_attributes = []
            for from_form in from_forms:
                from_attributes.append(set([ii for ii,jj in _dict_modules[from_form].attributes.items() if jj]))

            attributes_to_be_discarded = []
            for attribute in to_attributes:
                if attribute.startswith('n_'):
                    attributes_to_be_discarded.append(attribute)
            for attributes in from_attributes:
                for attribute in attributes:
                    if attribute.startswith('n_'):
                        attributes_to_be_discarded.append(attribute)

            attributes_to_be_discarded += ['box_volume', 'box_shape', 'box_angles', 'box_lengths']
            attributes_to_be_discarded += ['atom_index', 'structure_index']

            for attribute in attributes_to_be_discarded:
                to_attributes.discard(attribute)
                for ii in from_attributes:
                    ii.discard(attribute)

            all_from_attributes = set()
            all_from_attributes = all_from_attributes.union(*from_attributes)

        #### straight conversion

        if tmp_item is None:

            ## checking if there is useful straight conversions

            straight_conversions = {}

            for item_index in range(n_items):
                from_form = from_forms[item_index]
                aux_set = from_attributes[item_index]
                if from_form in _dict_modules:
                    if to_form in _dict_modules[from_form]._convert_to:

                        input_arguments = set(inspect.signature(_dict_modules[from_form]._convert_to[to_form]).parameters)
                        for ii in ['atom_indices', 'group_indices', 'component_indices', 'chain_indices',
                                'molecule_indices', 'entity_indices', 'structure_indices', 'molecular_system']:
                            input_arguments.discard(ii)

                        attributes_in_other_forms = {}
                        for aux_attribute in (all_from_attributes - aux_set) & to_attributes:
                            for ii in range(n_items-1,0,-1):
                                if has_attribute(molecular_system[ii], aux_attribute):
                                    attributes_in_other_forms[aux_attribute]=molecular_system[ii]
                                    break

                        repeated_attributes = {}
                        for aux_attribute in aux_set:
                            for ii in range(n_items-1, item_index, -1):
                                if aux_attribute in from_attributes[ii]:
                                    if has_attribute(molecular_system[ii], aux_attribute):
                                        repeated_attributes[aux_attribute]=molecular_system[ii]
                                        break

                        status_input_attributes = True
                        status_set_attributes = True

                        for aux_attribute in attributes_in_other_forms:
                            if not aux_attribute in input_arguments:
                                status_input_attributes = False
                                break

                        for aux_attribute in repeated_attributes:

                            if not (hasattr(_dict_modules[to_form], 'set_{aux_attribute}_to_system') or hasattr(_dict_modules[to_form], 'set_{aux_attribute}_to_atom')):
                                status_set_attributes = False
                                break

                        straight_conversions[from_form] = {
                                'input_arguments' : input_arguments,
                                'attributes_in_form' : aux_set,
                                'attributes_in_other_forms': attributes_in_other_forms,
                                'repeated_attributes': repeated_attributes,
                                'status_input_attributes': status_input_attributes,
                                'status_set_attributes': status_set_attributes,
                                }

            for straight_conversion in 

            print(straight_conversions)            
            

            #### through MolSys

            # with set

            #print(to_attributes)
            #print(from_attributes)

            pass


    # Returning the output

    if tmp_item is None:

        from_form = get_form(molecular_system)
        if len(from_form)==1:
            from_form=from_form[0]
        raise NotImplementedConversionError(from_form, to_form)

    if isinstance(tmp_item, (list, tuple)):
        if len(tmp_item) == 1:
            tmp_item = tmp_item[0]

    return tmp_item

    #######

    #if not isinstance(molecular_system, (list, tuple)):
    #    molecular_system = [molecular_system]

    #for item in molecular_system:

    #    from_form = get_form(item)

    #    if from_form == to_form:
    #        if from_form in ['molsysmt.MolecularMechanicsDict', 'molsysmt.MolecularMechanics']:
    #            tmp_item = dict_extract[from_form](item,
    #                                           copy_if_all=False,
    #                                           **conversion_arguments, **kwargs)
    #        else:
    #            tmp_item = dict_extract[from_form](item,
    #                                           atom_indices=atom_indices,
    #                                           structure_indices=structure_indices,
    #                                           copy_if_all=False,
    #                                           **conversion_arguments, **kwargs)
    #    else:
    #        if from_form in dict_convert:
    #            if to_form in dict_convert[from_form]:
    #                tmp_item = dict_convert[from_form][to_form](item,
    #                                                            molecular_system=molecular_system,
    #                                                            atom_indices=atom_indices,
    #                                                            structure_indices=structure_indices,
    #                                                            **conversion_arguments, **kwargs)
    #    if tmp_item is not None:
    #        break


