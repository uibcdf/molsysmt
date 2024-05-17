import numpy as np
import pandas as pd
from molsysmt._private.variables import is_all
from molsysmt._private.strings import get_parenthesis
from molsysmt.element import _plural_elements_to_singular, _element_index
from re import findall
from inspect import stack, getargvalues


def select(molecular_system, selection='all', structure_indices='all'):

    if isinstance(selection, str):

        while selection_with_special_subsentences(selection):

            sub_selection = selection_with_special_subsentences(selection)
            sub_atom_indices = select(molecular_system, sub_selection, structure_indices)
            selection = selection.replace(sub_selection, 'atom_index==@sub_atom_indices')

        if _in_elements_of(selection):

            atom_indices = select_in_elements_of(molecular_system, selection)

        elif 'within' in selection:

            atom_indices = select_within(molecular_system, selection, structure_indices)

        elif 'bonded to' in selection:

            atom_indices = select_bonded_to(molecular_system, selection)

        else:

            atom_indices = select_standard(molecular_system, selection)

    return atom_indices


def select_standard(item, selection):


    from molsysmt.basic import convert, get_form
    from molsysmt.config import selection_shortcuts
    from molsysmt.form import _dict_modules

    tmp_selection = selection

    shortcuts = selection_shortcuts['MolSysMT']

    for key in shortcuts:
        if key in selection:
            tmp_selection = tmp_selection.replace(key, shortcuts[key])



    form_in = get_form(item)

    if form_in == 'molsysmt.Topology':
        tmp_item = item
    else:

        conversion_needs_missing_bonds=False

        if isinstance(form_in, (list, tuple)):
            for ii in form_in:
                if (not _dict_modules[ii].bonds_are_explicit) and _dict_modules[ii].bonds_can_be_computed:
                    conversion_needs_missing_bonds=True
                    break
        else: 
            if (not _dict_modules[form_in].bonds_are_explicit) and _dict_modules[form_in].bonds_can_be_computed:
                conversion_needs_missing_bonds=True

        if conversion_needs_missing_bonds:

            from molsysmt.attribute.bonds_are_required_to_get_attribute import bond_dependent_attributes

            bonds_required_by_selection = False
            for attribute in bond_dependent_attributes:
                if attribute in tmp_selection:
                    bonds_required_by_selection = True
                    break

            tmp_item = convert(item, to_form='molsysmt.Topology', get_missing_bonds=bonds_required_by_selection,
                               skip_digestion=True)

        else:

            tmp_item = convert(item, to_form='molsysmt.Topology', skip_digestion=True)

    if '@' in selection:

        var_names = _var_names_in_selection(selection)

        all_stack_frames = stack()

        counter = -1
        n_frames = len(all_stack_frames)

        no_wrapper_stack_frames = [ii for ii in all_stack_frames if ii[3] != 'wrapper']

        for aux_stack in no_wrapper_stack_frames:
            args, args_paramname, kwargs_paramname, values = getargvalues(aux_stack.frame)
            if 'selection' in args:
                selection_input = values['selection']
                aux_var_names = _var_names_in_selection(selection_input)
                if all([ii in aux_var_names for ii in var_names]):
                    counter += 1
                else:
                    break
            else:
                break

        # print(counter)
        # for ii in range(len(no_wrapper_stack_frames)):
        #     aaa = no_wrapper_stack_frames[ii]
        #     print(ii, aaa[3])
        #     if 'selection' in getargvalues(aaa.frame)[3]:
        #         print('#####', getargvalues(aaa.frame)[3]['selection'])
        #     print('>>>', var_names[0] in aaa[0].f_locals)
        #     print('>>>', var_names[0] in aaa[0].f_globals)

        for var_name in var_names:
            if var_name in no_wrapper_stack_frames[counter][0].f_locals:
                var_value = no_wrapper_stack_frames[counter][0].f_locals[var_name]
            elif var_name in no_wrapper_stack_frames[counter][0].f_globals:
                var_value = no_wrapper_stack_frames[counter][0].f_globals[var_name]
            elif var_name in no_wrapper_stack_frames[counter+1][0].f_locals:
                var_value = no_wrapper_stack_frames[counter+1][0].f_locals[var_name]
            elif var_name in no_wrapper_stack_frames[counter+1][0].f_globals:
                var_value = no_wrapper_stack_frames[counter+1][0].f_globals[var_name]
            else:
                raise ValueError("The variable", var_name, "was not found by the selection tool.")
            tmp_selection = tmp_selection.replace('@'+var_name, '@auxiliar_variable_'+var_name)
            if type(var_value) in [np.ndarray]:
                var_value = list(var_value)
            locals()['auxiliar_variable_'+var_name]=var_value

    if is_all(tmp_selection):

        output = np.array(np.arange(tmp_item.atoms.shape[0]))

    else:

        atom_columns = []
        group_columns = []
        component_columns = []
        molecule_columns = []
        entity_columns = []
        chain_columns = []

        for column in tmp_item.atoms.keys():
            if column in tmp_selection:
                atom_columns.append(column)

        for column in tmp_item.groups.keys():
            if column in tmp_selection:
                group_columns.append(column)

        for column in tmp_item.components.keys():
            if column in tmp_selection:
                component_columns.append(column)

        for column in tmp_item.molecules.keys():
            if column in tmp_selection:
                molecule_columns.append(column)

        for column in tmp_item.entities.keys():
            if column in tmp_selection:
                entity_columns.append(column)

        for column in tmp_item.chains.keys():
            if column in tmp_selection:
                chain_columns.append(column)

        if len(entity_columns):
            if 'entity_index' not in molecule_columns:
                molecule_columns.append('entity_index')

        if len(molecule_columns):
            if 'molecule_index' not in component_columns:
                component_columns.append('molecule_index')

        if len(component_columns):
            if 'component_index' not in group_columns:
                group_columns.append('component_index')

        if len(group_columns):
            if 'group_index' not in atom_columns:
                atom_columns.append('group_index')

        if len(chain_columns):
            if 'chain_index' not in atom_columns:
                atom_columns.append('chain_index')

        aux_df = None

        if len(entity_columns):

            aux_df = pd.merge(tmp_item.molecules[molecule_columns], tmp_item.entities[entity_columns],
                              left_on='entity_index', right_index=True)

        if len(molecule_columns):

            if aux_df is None:

                aux_df = pd.merge(tmp_item.components[component_columns], tmp_item.molecules[molecule_columns],
                                  left_on='molecule_index', right_index=True)

            else:

                aux_df = pd.merge(tmp_item.components[component_columns], aux_df,
                                  left_on='molecule_index', right_index=True)

        if len(component_columns):

            if aux_df is None:

                aux_df = pd.merge(tmp_item.groups[group_columns], tmp_item.components[component_columns],
                                  left_on='component_index', right_index=True)

            else:

                aux_df = pd.merge(tmp_item.groups[group_columns], aux_df,
                                  left_on='component_index', right_index=True)

        if len(group_columns):

            if aux_df is None:

                aux_df = pd.merge(tmp_item.atoms[atom_columns], tmp_item.groups[group_columns],
                                  left_on='group_index', right_index=True)

            else:

                aux_df = pd.merge(tmp_item.atoms[atom_columns], aux_df,
                                  left_on='group_index', right_index=True)

        else:

            aux_df = tmp_item.atoms[atom_columns]

        if len(chain_columns):

            aux_df = pd.merge(aux_df, tmp_item.chains[chain_columns],
                              left_on='chain_index', right_index=True)

        tmp_selection = tmp_selection.replace('atom_index','index')
        output = aux_df.query(tmp_selection, engine='python').index.to_list()

        del aux_df

    return output


def select_within(molecular_system, selection, structure_indices):

    from molsysmt.structure.get_contacts import get_contacts

    not_within = False

    if "not within " in selection:
        selection_1, tmp_selection = selection.split(" not within ")
        not_within = True
    else:
        selection_1, tmp_selection = selection.split(" within ")

    pbc = False

    if "with pbc " in tmp_selection:
        pbc = True
        tmp_selection = tmp_selection.replace("with pbc ", "")
    elif "without pbc " in tmp_selection:
        tmp_selection = tmp_selection.replace("without pbc ", "")

    threshold, selection_2 = tmp_selection.split(" of ")

    atom_indices_1 = select(molecular_system, selection_1)
    atom_indices_2 = select(molecular_system, selection_2)
    cmap = get_contacts(molecular_system, selection=atom_indices_1, selection_2=atom_indices_2,
                        structure_indices=structure_indices, threshold=threshold, pbc=pbc)

    if not_within:
        output = np.array(atom_indices_1)[np.where(cmap.all(axis=2)[0] == False)[0]].tolist()
    else:
        output = np.array(atom_indices_1)[np.where(cmap.any(axis=2)[0] == True)[0]].tolist()

    return output


def select_bonded_to(molecular_system, selection):

    from molsysmt.basic import get

    not_bonded = False

    if "not bonded to" in selection:
        selection_1, selection_2 = selection.split(" not bonded to")
        not_bonded = True
    else:
        selection_1, selection_2 = selection.split(" bonded to")

    atom_indices_1 = select(molecular_system, selection=selection_1)
    atom_indices_2 = get(molecular_system, element='atom', selection=selection_2, bonded_atoms=True)
    atom_indices_2 = np.unique(np.concatenate(atom_indices_2).ravel())

    if not_bonded:
        output = np.setdiff1d(atom_indices_1, atom_indices_2, assume_unique=True).tolist()
    else:
        output = np.intersect1d(atom_indices_1, atom_indices_2, assume_unique=True).tolist()

    return output


_aux_dict_in_elements_in = {
        'groups': ['components',
                   'molecules',
                   'chains',
                   'entities'],
        'components': ['molecules',
                       'chains',
                       'entities'],
        'molecules': ['chains',
                      'entities'],
        'chains': ['molecules',
                   'entities'],
        'entities': [],
            }

#_aux_dict_in_elements_in = {
#        'entities': [],
#        'chains': ['molecules',
#                   'entities'],
#        'molecules': ['chains',
#                      'entities'],
#        'components': ['molecules',
#                       'chains',
#                       'entities'],
#        'groups': ['components',
#                   'molecules',
#                   'chains',
#                   'entities'],
#            }

def select_in_elements_of(molecular_system, selection):

    from molsysmt.basic import get

    for elements_1, list_elements_2 in _aux_dict_in_elements_in.items():

        if 'in '+elements_1 in selection:

            before, after = selection.split('in '+elements_1)

            before = before.strip()
            after = after.strip()

            if _in_elements_of(after):

                for elements_2 in list_elements_2:

                    if 'in '+elements_2 in after:

                        element_1 = _plural_elements_to_singular[elements_1]
                        element_2 = _plural_elements_to_singular[elements_2]

                        bbefore, aafter = after.split('in '+elements_2)

                        bbefore = bbefore.strip()
                        aafter = aafter.strip()

                        bbefore = bbefore.replace('of ', '')
                        aafter = aafter.replace('of ', '')

                        if bbefore == '':
                            bbefore = 'all'

                        if aafter == '':
                            aafter = 'all'

                        kwarg = {_element_index[element_1]: True}
                        pre_output = get(molecular_system, element=element_2, selection=aafter, skip_digestion=True,
                                         **kwarg)
                        if is_all(bbefore):
                            output_2 = pre_output
                        else:
                            mask = get(molecular_system, element=element_1, selection=bbefore, skip_digestion=True,
                                       **kwarg)
                            output_2 = [np.intersect1d(ii, mask).tolist() for ii in pre_output]
                        output_2 = [ii for ii in output_2 if len(ii) > 0]

                        output = []

                        aux_output_2 = np.concatenate(output_2).tolist()
                        pre_output = get(molecular_system, element=element_1, selection=aux_output_2, skip_digestion=True,
                                         atom_index=True)
                        aux_dict = {ii:jj for ii,jj in zip(aux_output_2, pre_output)}

                        if before == '':
                            before = 'all'

                        if is_all(before):
                            for aux_after in output_2:
                                pre_output = [aux_dict[ii] for ii in aux_after]
                                aux_output = [ii for ii in pre_output if len(ii) > 0]
                                output.append(aux_output)
                        else:
                            mask = select(molecular_system, selection=before)
                            for aux_after in output_2:
                                pre_output = [aux_dict[ii] for ii in aux_after]
                                aux_output = [np.intersect1d(ii, mask).tolist() for ii in pre_output]
                                aux_output = [ii for ii in aux_output if len(ii) > 0]
                                output.append(aux_output)

                        return output

            else:

                element_1 = _plural_elements_to_singular[elements_1]

                after = after.replace('of ', '')

                if before == '':
                    before = 'all'

                if after == '':
                    after = 'all'

                pre_output = get(molecular_system, element=element_1, selection=after, skip_digestion=True,
                                 atom_index=True)
                mask = select(molecular_system, selection=before)
                output = [np.intersect1d(ii, mask).tolist() for ii in pre_output]
                output = [ii for ii in output if len(ii) > 0]

                return output

    raise NotImplementedError


#def select_in_groups_of(molecular_system, selection):
#
#    from molsysmt.basic import get
#
#    before, after = selection.split('in groups of')
#    before = before.strip()
#    after = after.strip()
#
#    if before == '' or is_all(before):
#
#        output = get(molecular_system, element='group', selection=after, atom_index=True)
#        output = [ii for ii in output]
#
#    else:
#
#        pre_output = get(molecular_system, element='group', selection=after, atom_index=True)
#        mask = select(molecular_system, selection=before)
#        output = [np.intersect1d(ii, mask) for ii in pre_output]
#        output = [ii for ii in output if ii.shape[0] > 0]
#
#    return output


def selection_with_special_subsentences(selection):

    output = None
    parenthesis = get_parenthesis(selection)
    for subselection in parenthesis:
        if ('within ' in subselection) or ('bonded to ' in subselection):
            output = subselection
            break

    return output


def _var_names_in_selection(selection):

    var_names = []

    if isinstance(selection, str):

        var_names = [ii[1:] for ii in findall(r"@[\w']+", selection)]

    elif isinstance(selection, (tuple, list)):

        for ii in selection:

            var_names += _var_names_in_selection(ii)

    return var_names


def _in_elements_of(selection):

    output = False

    if "in groups" in selection:
        output = True
    elif "in components" in selection:
        output = True
    elif "in chains" in selection:
        output = True
    elif "in molecules" in selection:
        output = True
    elif "in entities" in selection:
        output = True

    return output
