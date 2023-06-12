from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def compare(molecular_system_A, molecular_system_B, selection_A='all', structure_indices_A='all',
        selection_B='all', structure_indices_B='all', attributes_type=None,
        syntax='MolSysMT', output_type='boolean', **kwargs):
    """
    Comparing molecular systems.

    Structures of a molecular system are appended to another molecular system.
    The indices of the structures from the source system
    (`from_molecular_system`) can be chosen by the input argument
    `structure_indices`. The number of atoms of the structures to be appended
    must be equal to the number of atoms of the target system
    (`to_molecular_system`). Otherwise, the input argument `selection` needs to
    be used to specify the atom indices or elements selected from the source
    system which structural attributes will be appended fulfilling this former condition.


    Parameters
    ----------
    to_molecular_system : molecular system
        Target molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Structures from the source molecular system will be appended to this system.

    from_molecular_system : molecular system
        Source molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Strucctures from this system will be appended to the target molecular system.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Atoms selection over which this method applies. The selection can be
        given by a list, tuple or numpy array of atom indices (0-based
        integers); or by means of a string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) of the source molecular system
        to get the structural attributes of the selected atoms, if any, to be
        appended.

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

    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.basic.convert(demo['alanine dipeptide']['alanine_dipeptide.msmpk'])
    >>> molecular_system_2 = msm.structure.translate(molecular_system_1, translation='[0.1, 0.1, 0.1] nanometers')
    >>> msm.basic.get(molecular_system_1, n_strctures=True)
    1
    >>> msm.basic.append_structures(molecular_system_1, molecular_system_2)
    >>> msm.basic.get(molecular_system_1, n_structures=True)
    2


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Append structures <Tutorial_Append_structures>`.    

    """

    rule='equal'

    # attributes: 'all', 'topological', 'structural', 'mechanical' 
    # output_type: 'boolean', 'dictionary'

    from molsysmt.basic import select, get, get_form, get_attributes
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, _topological_attributes, _structural_attributes, _mechanical_attributes

    output_dict = {}

    atts_to_be_compared = []

    atts_false = []

    if isinstance(attributes_type, str):
        if attributes_type == 'topological':
            atts_to_be_compared += _topological_attributes
        elif attributes_type == 'structural':
            atts_to_be_compared += _structural_attributes
        elif attributes_type == 'mechanical':
            atts_to_be_compared += _mechanical_attributes
        elif is_all(attributes_type):
            atts_to_be_compared += list(attributes.keys())

    for key in kwargs.keys():
        atts_to_be_compared.append(key)
        if not kwargs[key]:
            atts_false.append(key)

    if len(atts_to_be_compared)==0:
        atts_to_be_compared = ['n_atoms', 'atom_index', 'atom_id', 'atom_name', 'atom_type',
                'n_groups', 'group_index', 'group_id', 'group_name', 'group_type',
                'n_components', 'component_index', 'component_type',
                'n_molecules', 'molecule_index', 'molecule_type',
                'n_chains', 'chain_index', 'chain_id', 'chain_name', 'chain_type',
                'n_bonds', 'bonded_atoms',
                ]
        for key in kwargs.keys():
            if not kwargs[key]:
                if key in atts_to_be_compared:
                    atts_to_be_compared.remove(key)


    atts_of_A = get_attributes(molecular_system_A, output_type='list')
    atts_of_B = get_attributes(molecular_system_B, output_type='list')

    atts_required = set(atts_to_be_compared) & set(atts_of_A) & set(atts_of_B)

    ######   EQUAL   #####

    if rule == 'equal':

        ## n_atoms, atom_index, atom_name, atom_id, atom_type

        atts = atts_required & set(['n_atoms', 'atom_index', 'atom_id', 'atom_name', 'atom_type'])

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
                    output_dict['atom_id']= np.array_equal(dict_A['atom_id'], dict_B['atom_id'])

                if 'atom_name' in atts:
                    output_dict['atom_name']= np.array_equal(dict_A['atom_name'], dict_B['atom_name'])

                if 'atom_type' in atts:
                    output_dict['atom_type']= np.array_equal(dict_A['atom_type'], dict_B['atom_type'])

                del(dict_A, dict_B)

        ## n_groups, group_index, group_name, group_id, group_type

        atts = atts_required & set(['n_groups', 'group_index', 'group_id', 'group_name', 'group_type'])

        if len(atts)>0:

            n_groups_A = get(molecular_system_A, element='group', selection=selection_A,
                    syntax=syntax, n_groups=True)
            n_groups_B = get(molecular_system_B, element='group', selection=selection_B,
                    syntax=syntax, n_groups=True)

            if n_groups_A!=n_groups_B:

                for att in atts:
                    output_dict[att]=False

            else:

                if ('atom_index' in atts_of_A) and ('atom_index' in atts_of_B):

                    args = {ii:True for ii in atts if ii not in ['n_groups']}

                    dict_A = get(molecular_system_A, element='atom', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='atom', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_groups' in atts:
                        output_dict['n_groups']= (n_groups_A==n_groups_B)

                    if 'group_index' in atts:
                        output_dict['group_index']= np.array_equal(dict_A['group_index'], dict_B['group_index'])

                    if 'group_id' in atts:
                        output_dict['group_id']= np.array_equal(dict_A['group_id'], dict_B['group_id'])

                    if 'group_name' in atts:
                        output_dict['group_name']= np.array_equal(dict_A['group_name'], dict_B['group_name'])

                    if 'group_type' in atts:
                        output_dict['group_type']= np.array_equal(dict_A['group_type'], dict_B['group_type'])

                    del(dict_A, dict_B)


                else:

                    args = {ii:True for ii in atts if ii not in ['n_groups']}

                    dict_A = get(molecular_system_A, element='group', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='group', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_groups' in atts:
                        output_dict['n_groups']= (n_groups_A==n_groups_B)

                    if 'group_index' in atts:
                        output_dict['group_index']= np.array_equal(dict_A['group_index'], dict_B['group_index'])

                    if 'group_id' in atts:
                        output_dict['group_id']= np.array_equal(dict_A['group_id'], dict_B['group_id'])

                    if 'group_name' in atts:
                        output_dict['group_name']= np.array_equal(dict_A['group_name'], dict_B['group_name'])

                    if 'group_type' in atts:
                        output_dict['group_type']= np.array_equal(dict_A['group_type'], dict_B['group_type'])

                    del(dict_A, dict_B)

        ## n_components, component_index, component_name, component_id, component_type

        atts = atts_required & set(['n_components', 'component_index', 'component_id', 'component_name', 'component_type'])

        if len(atts)>0:

            n_components_A = get(molecular_system_A, element='component', selection=selection_A,
                    syntax=syntax, n_components=True)
            n_components_B = get(molecular_system_B, element='component', selection=selection_B,
                    syntax=syntax, n_components=True)

            if n_components_A!=n_components_B:

                for att in atts:
                    output_dict[att]=False

            else:

                if ('atom_index' in atts_of_A) and ('atom_index' in atts_of_B):

                    args = {ii:True for ii in atts if ii not in ['n_components']}

                    dict_A = get(molecular_system_A, element='component', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='component', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_components' in atts:
                        output_dict['n_components']= (n_components_A==n_components_B)

                    if 'component_index' in atts:
                        output_dict['component_index']= np.array_equal(dict_A['component_index'], dict_B['component_index'])

                    if 'component_id' in atts:
                        output_dict['component_id']= np.array_equal(dict_A['component_id'], dict_B['component_id'])

                    if 'component_name' in atts:
                        output_dict['component_name']= np.array_equal(dict_A['component_name'], dict_B['component_name'])

                    if 'component_type' in atts:
                        output_dict['component_type']= np.array_equal(dict_A['component_type'], dict_B['component_type'])

                    del(dict_A, dict_B)


                else:

                    args = {ii:True for ii in atts if ii not in ['n_components']}

                    dict_A = get(molecular_system_A, element='component', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='component', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_components' in atts:
                        output_dict['n_components']= (n_components_A==n_components_B)

                    if 'component_index' in atts:
                        output_dict['component_index']= np.array_equal(dict_A['component_index'], dict_B['component_index'])

                    if 'component_id' in atts:
                        output_dict['component_id']= np.array_equal(dict_A['component_id'], dict_B['component_id'])

                    if 'component_name' in atts:
                        output_dict['component_name']= np.array_equal(dict_A['component_name'], dict_B['component_name'])

                    if 'component_type' in atts:
                        output_dict['component_type']= np.array_equal(dict_A['component_type'], dict_B['component_type'])

                    del(dict_A, dict_B)

        ## n_molecules, molecule_index, molecule_name, molecule_id, molecule_type

        atts = atts_required & set(['n_molecules', 'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type'])

        if len(atts)>0:

            n_molecules_A = get(molecular_system_A, element='molecule', selection=selection_A,
                    syntax=syntax, n_molecules=True)
            n_molecules_B = get(molecular_system_B, element='molecule', selection=selection_B,
                    syntax=syntax, n_molecules=True)

            if n_molecules_A!=n_molecules_B:

                for att in atts:
                    output_dict[att]=False

            else:

                if ('atom_index' in atts_of_A) and ('atom_index' in atts_of_B):

                    args = {ii:True for ii in atts if ii not in ['n_molecules']}

                    dict_A = get(molecular_system_A, element='molecule', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='molecule', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_molecules' in atts:
                        output_dict['n_molecules']= (n_molecules_A==n_molecules_B)

                    if 'molecule_index' in atts:
                        output_dict['molecule_index']= np.array_equal(dict_A['molecule_index'], dict_B['molecule_index'])

                    if 'molecule_id' in atts:
                        output_dict['molecule_id']= np.array_equal(dict_A['molecule_id'], dict_B['molecule_id'])

                    if 'molecule_name' in atts:
                        output_dict['molecule_name']= np.array_equal(dict_A['molecule_name'], dict_B['molecule_name'])

                    if 'molecule_type' in atts:
                        output_dict['molecule_type']= np.array_equal(dict_A['molecule_type'], dict_B['molecule_type'])

                    del(dict_A, dict_B)


                else:

                    args = {ii:True for ii in atts if ii not in ['n_molecules']}

                    dict_A = get(molecular_system_A, element='molecule', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='molecule', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_molecules' in atts:
                        output_dict['n_molecules']= (n_molecules_A==n_molecules_B)

                    if 'molecule_index' in atts:
                        output_dict['molecule_index']= np.array_equal(dict_A['molecule_index'], dict_B['molecule_index'])

                    if 'molecule_id' in atts:
                        output_dict['molecule_id']= np.array_equal(dict_A['molecule_id'], dict_B['molecule_id'])

                    if 'molecule_name' in atts:
                        output_dict['molecule_name']= np.array_equal(dict_A['molecule_name'], dict_B['molecule_name'])

                    if 'molecule_type' in atts:
                        output_dict['molecule_type']= np.array_equal(dict_A['molecule_type'], dict_B['molecule_type'])

                    del(dict_A, dict_B)

        ## n_chains, chain_index, chain_name, chain_id, chain_type

        atts = atts_required & set(['n_chains', 'chain_index', 'chain_id', 'chain_name', 'chain_type'])

        if len(atts)>0:

            n_chains_A = get(molecular_system_A, element='chain', selection=selection_A,
                    syntax=syntax, n_chains=True)
            n_chains_B = get(molecular_system_B, element='chain', selection=selection_B,
                    syntax=syntax, n_chains=True)

            if n_chains_A!=n_chains_B:

                for att in atts:
                    output_dict[att]=False

            else:

                if ('atom_index' in atts_of_A) and ('atom_index' in atts_of_B):

                    args = {ii:True for ii in atts if ii not in ['n_chains']}

                    dict_A = get(molecular_system_A, element='chain', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='chain', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_chains' in atts:
                        output_dict['n_chains']= (n_chains_A==n_chains_B)

                    if 'chain_index' in atts:
                        output_dict['chain_index']= np.array_equal(dict_A['chain_index'], dict_B['chain_index'])

                    if 'chain_id' in atts:
                        output_dict['chain_id']= np.array_equal(dict_A['chain_id'], dict_B['chain_id'])

                    if 'chain_name' in atts:
                        output_dict['chain_name']= np.array_equal(dict_A['chain_name'], dict_B['chain_name'])

                    if 'chain_type' in atts:
                        output_dict['chain_type']= np.array_equal(dict_A['chain_type'], dict_B['chain_type'])

                    del(dict_A, dict_B)


                else:

                    args = {ii:True for ii in atts if ii not in ['n_chains']}

                    dict_A = get(molecular_system_A, element='chain', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='chain', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_chains' in atts:
                        output_dict['n_chains']= (n_chains_A==n_chains_B)

                    if 'chain_index' in atts:
                        output_dict['chain_index']= np.array_equal(dict_A['chain_index'], dict_B['chain_index'])

                    if 'chain_id' in atts:
                        output_dict['chain_id']= np.array_equal(dict_A['chain_id'], dict_B['chain_id'])

                    if 'chain_name' in atts:
                        output_dict['chain_name']= np.array_equal(dict_A['chain_name'], dict_B['chain_name'])

                    if 'chain_type' in atts:
                        output_dict['chain_type']= np.array_equal(dict_A['chain_type'], dict_B['chain_type'])

                    del(dict_A, dict_B)

        ## n_entities, entity_index, entity_name, entity_id, entity_type

        atts = atts_required & set(['n_entities', 'entity_index', 'entity_id', 'entity_name', 'entity_type'])

        if len(atts)>0:

            n_entities_A = get(molecular_system_A, element='entity', selection=selection_A,
                    syntax=syntax, n_entities=True)
            n_entities_B = get(molecular_system_B, element='entity', selection=selection_B,
                    syntax=syntax, n_entities=True)

            if n_entities_A!=n_entities_B:

                for att in atts:
                    output_dict[att]=False

            else:

                if ('atom_index' in atts_of_A) and ('atom_index' in atts_of_B):

                    args = {ii:True for ii in atts if ii not in ['n_entities']}

                    dict_A = get(molecular_system_A, element='entity', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='entity', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_entities' in atts:
                        output_dict['n_entities']= (n_entities_A==n_entities_B)

                    if 'entity_index' in atts:
                        output_dict['entity_index']= np.array_equal(dict_A['entity_index'], dict_B['entity_index'])

                    if 'entity_id' in atts:
                        output_dict['entity_id']= np.array_equal(dict_A['entity_id'], dict_B['entity_id'])

                    if 'entity_name' in atts:
                        output_dict['entity_name']= np.array_equal(dict_A['entity_name'], dict_B['entity_name'])

                    if 'entity_type' in atts:
                        output_dict['entity_type']= np.array_equal(dict_A['entity_type'], dict_B['entity_type'])

                    del(dict_A, dict_B)


                else:

                    args = {ii:True for ii in atts if ii not in ['n_entities']}

                    dict_A = get(molecular_system_A, element='entity', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='entity', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    if 'n_entities' in atts:
                        output_dict['n_entities']= (n_entities_A==n_entities_B)

                    if 'entity_index' in atts:
                        output_dict['entity_index']= np.array_equal(dict_A['entity_index'], dict_B['entity_index'])

                    if 'entity_id' in atts:
                        output_dict['entity_id']= np.array_equal(dict_A['entity_id'], dict_B['entity_id'])

                    if 'entity_name' in atts:
                        output_dict['entity_name']= np.array_equal(dict_A['entity_name'], dict_B['entity_name'])

                    if 'entity_type' in atts:
                        output_dict['entity_type']= np.array_equal(dict_A['entity_type'], dict_B['entity_type'])

                    del(dict_A, dict_B)


        ## n_bonds, bond_index, bond_order, bond_id, bond_type
        ## bonded_atoms, inner_bonded_atoms, inner_bond_index
        ## n_inner_bonds

        atts = atts_required & set(['n_bonds', 'bond_index', 'bond_id', 'bond_order', 'bond_type',
            'bonded_atoms', 'inner_bonded_atoms', 'inner_bond_index', 'n_inner_bonds'])

        if len(atts)>0:

            n_bonds_A = get(molecular_system_A, element='bond', selection=selection_A,
                    syntax=syntax, n_bonds=True)
            n_bonds_B = get(molecular_system_B, element='bond', selection=selection_B,
                    syntax=syntax, n_bonds=True)

            if n_bonds_A!=n_bonds_B:

                for att in atts:
                    output_dict[att]=False

            else:

                args = {ii:True for ii in atts if ii in ['n_bonds', 'bonded_atoms', 'bond_index',
                    'bond_id', 'bond_order', 'bond_type']}

                if len(args)>0:

                    if 'bonded_atoms' not in args:
                        args['bonded_atoms']=True

                    dict_A = get(molecular_system_A, element='bond', selection=selection_A,
                            syntax=syntax, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='bond', selection=selection_B,
                            syntax=syntax, output_type='dictionary', **args)

                    atoms_pairs_A = dict_A['bonded_atoms']
                    atoms_pairs_B = dict_B['bonded_atoms']
                    order_in_A = np.lexsort((atoms_pairs_A[:, 1], atoms_pairs_A[:, 0]))
                    order_in_B = np.lexsort((atoms_pairs_B[:, 1], atoms_pairs_B[:, 0]))

                    if 'n_bonds' in atts:
                        output_dict['n_bonds']= (n_bonds_A==n_bonds_B)

                    if 'bond_index' in atts:

                        output_dict['bond_index']= np.array_equal(dict_A['bond_index'][order_in_A], dict_B['bond_index'][order_in_B])

                    if 'bond_id' in atts:
                        output_dict['bond_id']= np.array_equal(dict_A['bond_id'][order_in_A], dict_B['bond_id'][order_in_B])

                    if 'bond_order' in atts:
                        output_dict['bond_order']= np.array_equal(dict_A['bond_order'][order_in_A], dict_B['bond_order'][order_in_B])

                    if 'bond_type' in atts:
                        output_dict['bond_type']= np.array_equal(dict_A['bond_type'][order_in_A], dict_B['bond_type'][order_in_B])

                    if 'bonded_atoms' in atts:
                        output_dict['bonded_atoms']= np.array_equal(dict_A['bonded_atoms'][order_in_A], dict_B['bonded_atoms'][order_in_B])

                    del(dict_A, dict_B)

                args = {ii:True for ii in atts if ii in ['inner_bonded_atoms', 'inner_bond_index', 'n_inner_bonds']}

                if len(args)>0:

                    if 'inner_bonded_atoms' not in args:
                        args['inner_bonded_atoms']=True

                    need_inner = True

                    if is_all(selection_A) and is_all(selection_B):

                        need_inner = False

                        if (need_inner==False) and ('n_inner_bonds' in atts):
                            if 'n_bonds' in atts:
                                output_dict['n_inner_bonds']=output_dict['n_bonds']
                            else:
                                need_inner = True

                        if (need_inner==False) and ('inner_bond_index' in atts):
                            if 'bond_index' in atts:
                                output_dict['inner_bond_index']=output_dict['bond_index']
                            else:
                                need_inner = True

                        if (need_inner==False) and ('inner_bonded_atoms' in atts):
                            if 'bonded_atoms' in atts:
                                output_dict['inner_bonded_atoms']=output_dict['bonded_atoms']
                            else:
                                need_inner = True

                    if need_inner:

                        dict_A = get(molecular_system_A, element='atom', selection=selection_A,
                                syntax=syntax, output_type='dictionary', **args)
                        dict_B = get(molecular_system_B, element='atom', selection=selection_B,
                                syntax=syntax, output_type='dictionary', **args)

                        atoms_pairs_A = dict_A['inner_bonded_atoms']
                        atoms_pairs_B = dict_B['inner_bonded_atoms']
                        order_in_A = np.lexsort((atoms_pairs_A[:, 1], atoms_pairs_A[:, 0]))
                        order_in_B = np.lexsort((atoms_pairs_B[:, 1], atoms_pairs_B[:, 0]))

                        if 'n_inner_bonds' in atts:
                            output_dict['n_inner_bonds']= (dict_A['n_inner_bonds'] == dict_B['n_inner_bonds'])

                        if 'inner_bond_index' in atts:
                            output_dict['inner_bond_index']= np.array_equal(dict_A['inner_bond_index'], dict_B['inner_bond_index'])

                        if 'inner_bonded_atoms' in atts:
                            output_dict['inner_bonded_atoms']= np.array_equal(dict_A['inner_bonded_atoms'][order_in_A], dict_B['inner_bonded_atoms'][order_in_B])

                        del(dict_A, dict_B)

        ## n_structures, structure_index, structure_id, coordinates, velocities, box

        atts = atts_required & set(['n_structures', 'structure_index', 'structure_id',
            'coordinates', 'velocities', 'box', 'box_shape', 'box_angles', 'box_lengths',
            'box_volume'])

        if len(atts)>0:

            n_structures_A = get(molecular_system_A, element='system', selection=selection_A,
                    structure_indices=structure_indices_A, syntax=syntax, n_structures=True)

            n_structures_B = get(molecular_system_B, element='system', selection=selection_B,
                    structure_indices=structure_indices_B, syntax=syntax, n_structures=True)

            if n_structures_A!=n_structures_B:

                for att in atts:
                    output_dict[att]=False

            else:

                args = {ii:True for ii in atts if ii in ['n_structures', 'structure_indices']}

                if len(args)>0:

                    dict_A = get(molecular_system_A, element='system',
                            structure_indices=structure_indices_A, output_type='dictionary', **args)
                    dict_B = get(molecular_system_B, element='system',
                            structure_indices=structure_indices_B, output_type='dictionary', **args)

                    if 'n_structures' in atts:
                        output_dict['n_structures']= (n_structures_A==n_structures_B)

                    if 'structure_index' in atts:
                        output_dict['structure_index']= np.array_equal(dict_A['structure_index'], dict_B['structure_index'])

                    if 'structure_id' in atts:
                        output_dict['structure_id']= np.array_equal(dict_A['structure_id'], dict_B['structure_id'])

                    del(dict_A, dict_B)

                args = {ii:True for ii in atts if ii in ['coordinates', 'velocities']}

                if len(args)>0:

                    n_atoms_A = get(molecular_system_A, element='atom', selection=selection_A,
                            syntax=syntax, n_atoms=True)
                    n_atoms_B = get(molecular_system_B, element='atom', selection=selection_B,
                            syntax=syntax, n_atoms=True)

                    if n_atoms_A!=n_atoms_B:

                        if 'coordinates' in atts:
                            output_dict['coordinates']=False

                        if 'velocities' in atts:
                            output_dict['velocities']=False

                    else:

                        dict_A = get(molecular_system_A, element='atom', selection=selection_A,
                                structure_indices=structure_indices_A, syntax=syntax, output_type='dictionary', **args)
                        dict_B = get(molecular_system_B, element='atom', selection=selection_B,
                                structure_indices=structure_indices_B, syntax=syntax, output_type='dictionary', **args)

                        if 'coordinates' in atts:

                            if dict_A['coordinates'] is None:
                                if dict_B['coordinates'] is None:
                                    output_dict['coordinates']=True
                                else:
                                    output_dict['coordinates']=False
                            else:
                                if dict_B['coordinates'] is None:
                                    output_dict['coordinates']=False
                                else:
                                    output_dict['coordinates'] = np.allclose(dict_A['coordinates'], dict_B['coordinates'])

                        if 'velocities' in atts:
                            if dict_A['velocities'] is None:
                                if dict_B['velocities'] is None:
                                    output_dict['velocities']=True
                                else:
                                    output_dict['velocities']=False
                            else:
                                if dict_B['velocities'] is None:
                                    output_dict['velocities']=False
                                else:
                                    output_dict['velocities'] = np.allclose(dict_A['velocities'], dict_B['velocities'])

                        del(dict_A, dict_B)

                args = {ii:True for ii in atts if ii in ['box', 'box_shape', 'box_volume',
                    'box_lengths', 'box_angles', 'box_volume']}

                if len(args)>0:

                    box_A = get(molecular_system_A, element='system',
                            structure_indices=structure_indices_A, box=True)
                    box_B = get(molecular_system_B, element='system',
                            structure_indices=structure_indices_B, box=True)

                    equal_box = False
                    if box_A is None:
                        if box_B is None:
                            equal_box = True
                        else:
                            equal_box = False
                    else:
                        if box_B is None:
                            equal_box = False
                        else:
                            equal_box = np.allclose(box_A, box_B)

                    if 'box' in atts:
                        output_dict['box']=equal_box

                    if 'box_shape' in atts:
                        output_dict['box_shape']=equal_box

                    if 'box_volume' in atts:
                        output_dict['box_volume']=equal_box

                    if 'box_lengths' in atts:
                        output_dict['box_lengths']=equal_box

                    if 'box_angles' in atts:
                        output_dict['box_angles']=equal_box

                    del(box_A, box_B)

    elif rule == 'in':

        raise NotImplementedMethodError()


    for att_false in atts_false:
        if att_false in output_dict:
            if output_dict[att_false]:
                output_dict[att_false]=False
            else:
                output_dict[att_false]=True

    if output_type=='boolean':

        return np.all(list(output_dict.values()))

    elif output_type=='dictionary':

        return {ii:output_dict[ii] for ii in attributes if ii in output_dict}

