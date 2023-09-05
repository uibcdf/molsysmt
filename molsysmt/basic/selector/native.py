from molsysmt._private.exceptions import NotImplementedMethodError, NotSupportedSyntaxError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt._private.strings import get_parenthesis
from re import findall
from inspect import stack, getargvalues


def select(molecular_system, selection, structure_indices):

    if isinstance(selection, str):

        while selection_with_special_subsentences(selection):

            sub_selection = selection_with_special_subsentences(selection)
            sub_atom_indices = select(molecular_system, sub_selection, structure_indices)
            selection = selection.replace(sub_selection, 'atom_index==@sub_atom_indices')

        if 'in groups of' in selection:
            atom_indices = select_in_groups_of(molecular_system, selection)

        elif 'in components of' in selection:
            atom_indices = select_in_components_of(molecular_system, selection)

        elif 'in molecules of' in selection:
            atom_indices = select_in_molecules_of(molecular_system, selection)

        elif 'in chains of' in selection:
            atom_indices = select_in_chains_of(molecular_system, selection)

        elif 'in entities of' in selection:
            atom_indices = select_in_entities_of(molecular_system, selection)

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

    form_in = get_form(item)

    if form_in == 'molsysmt.Topology':
        tmp_item = item
    else:
        tmp_item = convert(item, to_form='molsysmt.Topology')

    tmp_selection = selection

    if '@' in selection:

        var_names = [ii[1:] for ii in findall(r"@[\w']+", selection)]

        all_stack_frames = stack()

        counter = -1
        n_frames = len(all_stack_frames)

        no_wrapper_stack_frames = [ii for ii in all_stack_frames if ii[3]!='wrapper']

        for aux_stack in no_wrapper_stack_frames:
            args, args_paramname, kwargs_paramname, values = getargvalues(aux_stack.frame)
            if 'selection' in args:
                counter+=1
            else:
                break

        #print(counter)
        #for ii in range(len(no_wrapper_stack_frames)):
        #    aaa = no_wrapper_stack_frames[ii]
        #    print(ii, aaa[3])
        #    if 'selection' in getargvalues(aaa.frame)[3]:
        #        print('#####', getargvalues(aaa.frame)[3]['selection'])
        #    print('>>>', var_names[0] in aaa[0].f_locals)
        #    print('>>>', var_names[0] in aaa[0].f_globals)

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

    shortcuts = selection_shortcuts['MolSysMT']

    for key in shortcuts:
        if key in selection:
            tmp_selection = tmp_selection.replace(key, shortcuts[key])

    output = tmp_item.atoms_dataframe.query(tmp_selection).index.to_numpy()

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
        tmp_selection = tmp_selection.replace("with pbc ","")
    elif "without pbc " in tmp_selection:
        tmp_selection = tmp_selection.replace("without pbc ","")

    threshold, selection_2 = tmp_selection.split(" of ")

    atom_indices_1 = select(molecular_system, selection=selection_1)
    atom_indices_2 = select(molecular_system, selection=selection_2)
    cmap = get_contacts(molecular_system, selection=atom_indices_1, selection_2=atom_indices_2,
            structure_indices=structure_indices, threshold=threshold, pbc=pbc, engine='MolSysMT')

    if not_within:
        output = atom_indices_1[np.where(cmap.all(axis=2)[0]==False)[0]]
    else:
        output = atom_indices_1[np.where(cmap.any(axis=2)[0]==True)[0]]

    return output


def select_bonded_to(molecular_system, selection):

    from molsysmt.basic import get

    not_bonded=False

    if "not bonded to" in selection:
        selection_1, selection_2 = selection.split(" not bonded to")
        not_bonded=True
    else:
        selection_1, selection_2 = selection.split(" bonded to")

    atom_indices_1 = select(molecular_system, selection=selection_1)
    atom_indices_2 = get(molecular_system, element='atom', selection=selection_2, bonded_atoms=True)
    atom_indices_2 = np.unique(np.concatenate(atom_indices_2).ravel())

    if not_bonded:
        output = np.setdiff1d(atom_indices_1, atom_indices_2, assume_unique=True)
    else:
        output = np.intersect1d(atom_indices_1, atom_indices_2, assume_unique=True)

    return output


def select_in_groups_of(molecular_system, selection):

    from molsysmt.basic import get

    before, after=selection.split('in groups of')
    before = before.strip()
    after = after.strip()

    if before=='' or is_all(before):

        output = get(molecular_system, element='group', selection=after, atom_index=True)

    else:

        pre_output = get(molecular_system, element='group', selection=after, atom_index=True)
        mask = select(molecular_system, element='atom', selection=before)
        output = [np.intersect1d(ii, mask).astype('object') for ii in pre_output]
        output = [ii for ii in output if ii.shape[0]>0]
        output = np.array(output, dtype='object')

    return output


def select_in_components_of(molecular_system, selection):

    from molsysmt.basic import get

    before, after=selection.split('in components of')
    before = before.strip()
    after = after.strip()

    if before=='' or is_all(before):

        output = get(molecular_system, element='component', selection=after, atom_index=True)

    else:

        pre_output = get(molecular_system, element='component', selection=after, atom_index=True)
        mask = select(molecular_system, element='atom', selection=before)
        output = [np.intersect1d(ii, mask).astype('object') for ii in pre_output]
        output = [ii for ii in output if ii.shape[0]>0]
        output = np.array(output, dtype='object')

    return output


def select_in_molecules_of(molecular_system, selection):

    from molsysmt.basic import get

    before, after=selection.split('in molecules of')
    before = before.strip()
    after = after.strip()

    if before=='' or is_all(before):

        output = get(molecular_system, element='molecule', selection=after, atom_index=True)

    else:

        pre_output = get(molecular_system, element='molecule', selection=after, atom_index=True)
        mask = select(molecular_system, element='atom', selection=before)
        output = [np.intersect1d(ii, mask).astype('object') for ii in pre_output]
        output = [ii for ii in output if ii.shape[0]>0]
        output = np.array(output, dtype='object')

    return output


def select_in_chains_of(molecular_system, selection):

    from molsysmt.basic import get

    before, after=selection.split('in chains of')
    before = before.strip()
    after = after.strip()

    if before=='' or is_all(before):

        output = get(molecular_system, element='chain', selection=after, atom_index=True)

    else:

        pre_output = get(molecular_system, element='chain', selection=after, atom_index=True)
        mask = select(molecular_system, element='atom', selection=before)
        output = [np.intersect1d(ii, mask).astype('object') for ii in pre_output]
        output = [ii for ii in output if ii.shape[0]>0]
        output = np.array(output, dtype='object')

    return output


def select_in_entities_of(molecular_system, selection):

    from molsysmt.basic import get

    before, after=selection.split('in entities of')
    before = before.strip()
    after = after.strip()

    if before=='' or is_all(before):

        output = get(molecular_system, element='entity', selection=after, atom_index=True)

    else:

        pre_output = get(molecular_system, element='entity', selection=after, atom_index=True)
        mask = select(molecular_system, element='atom', selection=before)
        output = [np.intersect1d(ii, mask).astype('object') for ii in pre_output]
        output = [ii for ii in output if ii.shape[0]>0]
        output = np.array(output, dtype='object')

    return output


def selection_with_special_subsentences(selection):

    output = None
    parenthesis = get_parenthesis(selection)
    for subselection in parenthesis:
        if ('within ' in subselection) or ('bonded to ' in subselection):
            output = subselection
            break

    return output


