from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
import numpy as np

@digest()
def compare(molecular_system_A, molecular_system_B, selection_A='all', structure_indices_A='all',
        selection_B='all', structure_indices_B='all', rule='equal', attributes_type=None,
        syntax='MolSysMT', output_type='boolean', minor_elements_included=True, **kwargs):

    # attributes: 'all', 'topological', 'structural', 'mechanical' 
    # output_type: 'boolean', 'dictionary'

    from molsysmt.basic import select, get, get_form, get_attributes
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, topological_attributes, structural_attributes, mechanical_attributes

    output_dict = {}

    atts_to_be_compared = []

    if isinstance(attributes_type):
        if attributes_type == 'topological':
            atts_to_be_compared += topological_attributes
        elif attributes_type == 'structural':
            atts_to_be_compared += structural_attributes
        elif attributes_type == 'mechanical':
            atts_to_be_compared += mechanical_attributes

    for key in kwargs.keys():
        if kwargs[key]:
            if key not in atts_to_be_compared:
                atts_to_be_compared.append(key)
        if not kwargs[key]:
            if key in atts_to_be_compared:
                atts_to_be_compared.remove(key)

    if len(atts_to_be_compared)==0:
        atts_to_be_compared = list(attributes.keys())
        for key in kwargs.keys():
            if not kwargs[key]:
                if key in atts_to_be_compared:
                    atts_to_be_compared.remove(key)


    atts_of_A = get_attributes(molecular_system_A)
    atts_of_B = get_attributes(molecular_system_B)

    atts_required = set(atts_to_be_compared) & set(atts_of_A) & set(atts_of_B)

    ######   EQUAL   #####

    if rule == 'equal':

        ## n_atoms, atom_index, atom_name, atom_id, atom_type

        atts = atts_required & set(['n_atoms', 'atom_index', 'atom_id', 'atom_type'])

        if len(atts)>0:

            n_atoms_A = get(molecular_system_A, element='atom', selection=selection_A,
                    syntax=syntax, n_atoms=True)
            n_atoms_B = get(molecular_system_A, element='atom', selection=selection_B,
                    syntax=syntax, n_atoms=True)

            if n_atoms_A!=n_atoms_B:

                for att in atts:
                    output_dict[att]=False

            else:

                args = {ii:True for ii in atts if ii not in ['n_atoms', 'atom_index']}

                dict_A = get(molecular_system_A, element='atom', selection=selection_A,
                        syntax=syntax, output_type='dictionary', **args)
                dict_B = get(molecular_system_B, element='atom', selection=selection_B,
                        syntax=syntax, output_type='dictionary', **args)

                if 'n_atoms' in atts:
                    output_dict['n_atoms']= True

                if 'atom_index' in atts:
                    output_dict['atom_index']= True

                if 'atom_id' in atts:
                    output_dict['atom_id']= np.all(dict_A['atom_id'] == dict_B['atom_id'])

                if 'atom_name' in atts:
                    output_dict['atom_name']= np.all(dict_A['atom_name'] == dict_B['atom_name'])

                if 'atom_type' in atts:
                    output_dict['atom_type']= np.all(dict_A['atom_type'] == dict_B['atom_type'])

                del(dict_A, dict_B)

        ## n_groups, group_index, group_name, group_id, group_type

        atts = atts_required & set(['n_groups', 'group_index', 'group_id', 'group_type'])

        if len(atts)>0:

            n_groups_A = get(molecular_system_A, element='group', selection=selection_A,
                    syntax=syntax, n_groups=True)
            n_groups_B = get(molecular_system_A, element='group', selection=selection_B,
                    syntax=syntax, n_groups=True)

            if n_groups_A!=n_groups_B:

                for att in atts:
                    output_dict[att]=False

            else:

                args = {ii:True for ii in atts if ii not in ['n_groups', 'group_index']}

                dict_A = get(molecular_system_A, element='group', selection=selection_A,
                        syntax=syntax, output_type='dictionary', **args)
                dict_B = get(molecular_system_B, element='group', selection=selection_B,
                        syntax=syntax, output_type='dictionary', **args)

                if 'n_groups' in atts:
                    output_dict['n_group']= True

                if 'group_index' in atts:
                    output_dict['group_index']= True

                if 'group_id' in atts:
                    output_dict['group_id']= np.all(dict_A['group_id'] == dict_B['group_id'])

                if 'group_name' in atts:
                    output_dict['group_name']= np.all(dict_A['group_name'] == dict_B['group_name'])

                if 'group_type' in atts:
                    output_dict['group_type']= np.all(dict_A['group_type'] == dict_B['group_type'])

                del(dict_A, dict_B)

                if minor_elements_included:

                    # equal atoms in groups

                    atts_in_minor = [ii for ii in atts if output_dict[ii]]

                    args = {ii:True for ii in atts_in_minor if ii not in ['n_groups']}

                    dict_A = get(molecular_system_A, element='group', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='group', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if group_index in atts_in_minor:
                        output_dict['group_index']= np.all(dict_A['group_index'] == dict_B['group_index'])

                    if group_id in atts_in_minor:
                        output_dict['group_id']= np.all(dict_A['group_id'] == dict_B['group_id'])

                    if group_name in atts_in_minor:
                        output_dict['group_name']= np.all(dict_A['group_name'] == dict_B['group_name'])

                    if group_type in atts_in_minor:
                        output_dict['group_type']= np.all(dict_A['group_type'] == dict_B['group_type'])

                    del(dict_A, dict_B)


            #### bonds

            ###if report_dict['n_bonds']:

            ###    bonded_atoms_A = get(molecular_system_A, element='atom', selection=selection_A, bonded_atoms=True)
            ###    bonded_atoms_B = get(molecular_system_B, element='atom', selection=selection_B, bonded_atoms=True)

            ###    report_dict['bonded_atoms'] = True
            ###    for ii,jj in zip(bonded_atoms_A, bonded_atoms_B):
            ###        if not np.all(ii==jj):
            ###            report_dict['bonded_atoms'] = False
            ###            break

            ###    if report_dict['bonded_atoms']:

            ###        atoms_pairs_A, bond_order_A, bond_type_A = get(molecular_system_A, element='bond', selection=selection_A,
            ###                                                   bonded_atoms=True, bond_order=True, bond_type=True)

            ###        atoms_pairs_B, bond_order_B, bond_type_B = get(molecular_system_B, element='bond', selection=selection_A,
            ###                                                   bonded_atoms=True, bond_order=True, bond_type=True)

            ###        order_in_A = np.lexsort((atoms_pairs_A[:, 1], atoms_pairs_A[:, 0]))
            ###        order_in_B = np.lexsort((atoms_pairs_B[:, 1], atoms_pairs_B[:, 0]))

            ###        check_bond_order = True 
            ###        check_bond_type = True 

            ###        for in_A, in_B in zip(order_in_A, order_in_B):
            ###            if check_bond_order:
            ###                check_bond_order = (bond_order_A[in_A]==bond_order_B[in_B])
            ###            if check_bond_type:
            ###                check_bond_type = (bond_type_A[in_A]==bond_type_B[in_B])
            ###            if check_bond_order == False and check_bond_type == False:
            ###                break

            ###        report_dict['bond_order'] = check_bond_order
            ###        report_dict['bond_type'] = check_bond_type

            ###    else:

            ###        report_dict['bond_order'] = False
            ###        report_dict['bond_type'] = False

            ###else:

            ###    report_dict['bonded_atoms'] = False
            ###    report_dict['bond_order'] = False
            ###    report_dict['bond_type'] = False

        ###if coordinates:

        ###    if report_dict['n_atoms']:

        ###        coordinates_A = get(molecular_system_A, element='atom', selection=selection_A,
        ###                            structure_indices=structure_indices_A, coordinates=True,
        ###                            )

        ###        coordinates_B = get(molecular_system_B, element='atom', selection=selection_B,
        ###                            structure_indices=structure_indices_B, coordinates=True,
        ###                            )

        ###        if coordinates_A is None:
        ###            if coordinates_B is None:
        ###                report_dict['coordinates'] = True
        ###            else:
        ###                report_dict['coordinates'] = False
        ###        else:
        ###            if coordinates_B is None:
        ###                report_dict['coordinates'] = False
        ###            else:
        ###                report_dict['coordinates'] = np.allclose(coordinates_A, coordinates_B)

        ###    else:

        ###        report_dict['coordinates'] = False

        ###if box:

        ###    box_A = get(molecular_system_A, element='system', selection=selection_A, structure_indices=structure_indices_A,
        ###                box=True)

        ###    box_B = get(molecular_system_B, element='system', selection=selection_B, structure_indices=structure_indices_B,
        ###                box=True)

        ###    if box_A is None:
        ###        if box_B is None:
        ###            report_dict['box'] = True
        ###        else:
        ###            report_dict['box'] = False
        ###    else:
        ###        if box_B is None:
        ###            report_dict['box'] = False
        ###        else:
        ###            report_dict['box'] = np.allclose(box_A, box_B)

    elif rule == 'in':

        raise NotImplementedMethodError()

    if output_type=='boolean':

        return result, report_dict

    elif output_type=='dictionary':

        return {ii:output[ii] for ii in attributes if ii in output}

