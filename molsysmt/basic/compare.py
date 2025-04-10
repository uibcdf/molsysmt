from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
import numpy as np

from time import time

@digest()
def compare(molecular_system, molecular_system_2, selection='all', structure_indices='all',
        selection_2='all', structure_indices_2='all',  syntax='MolSysMT', rule='equal',
        output_type='boolean', attribute_type=None, **kwargs):
    """
    Compare two molecular systems or parts of them.

    This function compares the attributes of two molecular systems or their selected subsets.
    The comparison can be performed according to two rules: equality (``'equal'``) or containment (``'in'``).
    You can restrict the comparison to specific elements and structures using the `selection`, 
    `structure_indices`, `selection_2`, and `structure_indices_2` arguments.

    If no specific attributes are passed as keyword arguments, all attributes—or those filtered by
    `attribute_type`—are considered.

    Parameters
    ----------
    molecular_system : molecular system
        The first molecular system to compare. It can be provided in any of the 
        :ref:`supported forms <Introduction_Forms>`.

    molecular_system_2 : molecular system
        The second molecular system to compare. Also accepted in any of the 
        :ref:`supported forms <Introduction_Forms>`.

    selection : str, list, tuple or ndarray, default='all'
        Elements to include from the first molecular system. Can be a string following a 
        :ref:`supported selection syntax <Introduction_Selection>` or a list/array of atom indices (0-based).

    structure_indices : str, list, tuple or ndarray, default='all'
        Structures to include from the first molecular system (0-based indices).

    selection_2 : str, list, tuple or ndarray, default='all'
        Elements to include from the second molecular system. Same syntax as `selection`.

    structure_indices_2 : str, list, tuple or ndarray, default='all'
        Structures to include from the second molecular system (0-based indices).

    syntax : str, default='MolSysMT'
        Syntax to interpret the `selection` and `selection_2` strings. 
        See :ref:`selection syntaxes <Introduction_Selection>`.

    rule : {'equal', 'in'}, default='equal'
        Rule to apply in the comparison:
        
        * `'equal'` — checks if values are identical.
        * `'in'` — checks if values of the first system are contained in the second.

    output_type : {'boolean', 'dictionary'}, default='boolean'
        Format of the output:
        
        * `'boolean'` — returns a single True/False indicating global comparison success.
        * `'dictionary'` — returns a dict with per-attribute comparison results.

    attribute_type : {'topological', 'structural', 'mechanical', None}, default=None
        Category of attributes to compare. If not set, either attributes passed as keywords
        or all available attributes are considered.

        * 'topological': every :ref:`topological attribute <Introduction_Attributes>` in the systems is compared.
        * 'structural': every :ref:`structural attribute <Introduction_Attributes>` in the systems is compared.
        * 'mechanical': every :ref:`mechanical attribute <Introduction_Attributes>` in the systems is compared.
        * None: either all attributes introduced as additional keywords are compared (if any), or
          all attributes are compared if ``**kwargs==None``.

    **kwargs : dict, optional
        Attribute names to compare as keys, with boolean values indicating expected outcome:

        * `True` — the rule should hold (e.g. equality).
        * `False` — the negation of the rule should hold (e.g. inequality).

    Returns
    -------
    bool or dict
        Result of the comparison. A boolean if `output_type='boolean'`, or a dictionary
        of per-attribute results if `output_type='dictionary'`.

    Raises
    ------
    NotSupportedFormError
        If any molecular system is in an unsupported form.

    ArgumentError
        If input arguments are invalid.

    Notes
    -----
    For more information on forms and selection syntaxes, see:

    * :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`
    * :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.basic.select` : Select elements of a molecular system.
    :func:`molsysmt.get` : Retrieve attribute values.
    :func:`molsysmt.info` : Display system summary.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molsys_A = msm.convert(demo['T4 lysozyme L99A']['181l.h5msm'])
    >>> molsys_B = msm.convert(demo['T4 lysozyme L99A']['181l.h5msm'], selection='molecule_type=="protein"')
    >>> msm.compare(molsys_A, molsys_B)
    False
    >>> msm.compare(molsys_A, molsys_B, box=True)
    True
    >>> msm.compare(molsys_A, molsys_B, n_groups=False)
    True
    >>> msm.compare(molsys_A, molsys_B, selection='molecule_type=="protein"', n_groups=True)
    True

    .. admonition:: User guide

       See the full tutorial here: :ref:`User Guide > Tools > Basic > Compare <Tutorial_Compare>`

    .. versionadded:: 1.0.0
    """

    rule='equal'

    # attributes: 'all', 'topological', 'structural', 'mechanical' 
    # output_type: 'boolean', 'dictionary'

    from molsysmt.basic import select, get, get_form, get_attributes
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, _topological_attributes, _structural_attributes, _mechanical_attributes
    from molsysmt.basic.get import _piped_molecular_system

    output_dict = {}

    atts_to_be_compared = []

    atts_false = []

    if isinstance(attribute_type, str):
        if attribute_type == 'topological':
            atts_to_be_compared += _topological_attributes
        elif attribute_type == 'structural':
            atts_to_be_compared += _structural_attributes
        elif attribute_type == 'mechanical':
            atts_to_be_compared += _mechanical_attributes
        elif is_all(attribute_type):
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
                'n_bonds', 'bonded_atom_pairs',
                ]
        for key in kwargs.keys():
            if not kwargs[key]:
                if key in atts_to_be_compared:
                    atts_to_be_compared.remove(key)

    atts_of_A = get_attributes(molecular_system, output_type='list')
    atts_of_B = get_attributes(molecular_system_2, output_type='list')

    atts_required = set(atts_to_be_compared) & set(atts_of_A) & set(atts_of_B)

    piped_system_A, piped_atts_A = _piped_molecular_system(molecular_system, 'atom', atts_required)
    piped_system_B, piped_atts_B = _piped_molecular_system(molecular_system_2, 'atom', atts_required)

    dict_A = {}
    dict_B = {}

    aux = [
        ['atom', set(['n_atoms', 'atom_index', 'atom_id', 'atom_name', 'atom_type'])],
        ['group', set(['n_groups', 'group_index', 'group_id', 'group_name', 'group_type'])],
        ['component', set(['n_components', 'component_index', 'component_id', 'component_name', 'component_type'])],
        ['molecule', set(['n_molecules', 'molecule_index', 'molecule_id', 'molecule_name', 'molecule_type'])],
        ['chain', set(['n_chains', 'chain_index', 'chain_id', 'chain_name', 'chain_type'])],
        ['entity', set(['n_entities', 'entity_index', 'entity_id', 'entity_name', 'entity_type'])],
        ['bond',set(['n_bonds', 'bond_index', 'bond_id', 'bond_order', 'bond_type', 'bonded_atom_pairs'])],
        ['atom', set(['inner_bonded_atom_pairs', 'inner_bond_index', 'n_inner_bonds'])],
        ['atom',set(['coordinates', 'velocities'])],
        ['system',set(['n_structures', 'structure_index', 'structure_id', 'box',
                     'box_shape', 'box_angles', 'box_lengths', 'box_volume'])]
    ]

    for aux2 in aux:


        element=aux2[0]
        atts = atts_required & aux2[1]

        if piped_system_A is None:
            aux_molecular_system = molecular_system
        else:
            for aux_molecular_system, aux_atts in zip(piped_system_A, piped_atts_A):
                if atts.issubset(aux_atts):
                    break
            if aux_molecular_system is None:
                aux_molecular_system = molecular_system

        dict_aux = get(aux_molecular_system, element=element, selection=selection,
                       structure_indices=structure_indices, syntax=syntax,
                       output_type='dictionary', **{ii:True for ii in atts})

        dict_A.update(dict_aux)

        if piped_system_B is None:
            aux_molecular_system = molecular_system_2
        else:
            for aux_molecular_system, aux_atts in zip(piped_system_B, piped_atts_B):
                if atts.issubset(aux_atts):
                    break
            if aux_molecular_system is None:
                aux_molecular_system = molecular_system_2

        dict_aux = get(aux_molecular_system, element=element, selection=selection_2,
                       structure_indices=structure_indices_2, syntax=syntax,
                       output_type='dictionary', **{ii:True for ii in atts})

        dict_B.update(dict_aux)

    ######   EQUAL   #####

    if rule == 'equal':

        if 'n_atoms' in atts_required:
            output_dict['n_atoms']= (dict_A['n_atoms']==dict_B['n_atoms'])

        if 'atom_index' in atts_required:
            output_dict['atom_index']= np.array_equal(dict_A['atom_index'], dict_B['atom_index'])

        if 'atom_id' in atts_required:
            output_dict['atom_id']= np.array_equal(dict_A['atom_id'], dict_B['atom_id'])

        if 'atom_name' in atts_required:
            output_dict['atom_name']= np.array_equal(dict_A['atom_name'], dict_B['atom_name'])

        if 'atom_type' in atts_required:
            output_dict['atom_type']= np.array_equal(dict_A['atom_type'], dict_B['atom_type'])

        if 'n_groups' in atts_required:
            output_dict['n_groups']= (dict_A['n_groups']==dict_B['n_groups'])

        if 'group_index' in atts_required:
            output_dict['group_index']= np.array_equal(dict_A['group_index'], dict_B['group_index'])

        if 'group_id' in atts_required:
            output_dict['group_id']= np.array_equal(dict_A['group_id'], dict_B['group_id'])

        if 'group_name' in atts_required:
            output_dict['group_name']= np.array_equal(dict_A['group_name'], dict_B['group_name'])

        if 'group_type' in atts_required:
            output_dict['group_type']= np.array_equal(dict_A['group_type'], dict_B['group_type'])

        if 'n_components' in atts_required:
            output_dict['n_components']= (dict_A['n_components']==dict_B['n_components'])

        if 'component_index' in atts_required:
            output_dict['component_index']= np.array_equal(dict_A['component_index'], dict_B['component_index'])

        if 'component_id' in atts_required:
            output_dict['component_id']= np.array_equal(dict_A['component_id'], dict_B['component_id'])

        if 'component_name' in atts_required:
            output_dict['component_name']= np.array_equal(dict_A['component_name'], dict_B['component_name'])

        if 'component_type' in atts_required:
            output_dict['component_type']= np.array_equal(dict_A['component_type'], dict_B['component_type'])

        if 'n_molecules' in atts_required:
            output_dict['n_molecules']= (dict_A['n_molecules']==dict_B['n_molecules'])

        if 'molecule_index' in atts_required:
            output_dict['molecule_index']= np.array_equal(dict_A['molecule_index'], dict_B['molecule_index'])

        if 'molecule_id' in atts_required:
            output_dict['molecule_id']= np.array_equal(dict_A['molecule_id'], dict_B['molecule_id'])

        if 'molecule_name' in atts_required:
            output_dict['molecule_name']= np.array_equal(dict_A['molecule_name'], dict_B['molecule_name'])

        if 'molecule_type' in atts_required:
            output_dict['molecule_type']= np.array_equal(dict_A['molecule_type'], dict_B['molecule_type'])

        if 'n_chains' in atts_required:
            output_dict['n_chains']= (dict_A['n_chains']==dict_B['n_chains'])

        if 'chain_index' in atts_required:
            output_dict['chain_index']= np.array_equal(dict_A['chain_index'], dict_B['chain_index'])

        if 'chain_id' in atts_required:
            output_dict['chain_id']= np.array_equal(dict_A['chain_id'], dict_B['chain_id'])

        if 'chain_name' in atts_required:
            output_dict['chain_name']= np.array_equal(dict_A['chain_name'], dict_B['chain_name'])

        if 'chain_type' in atts_required:
            output_dict['chain_type']= np.array_equal(dict_A['chain_type'], dict_B['chain_type'])

        if 'n_entities' in atts_required:
            output_dict['n_entities']= (dict_A['n_entities']==dict_B['n_entities'])

        if 'entity_index' in atts_required:
            output_dict['entity_index']= np.array_equal(dict_A['entity_index'], dict_B['entity_index'])

        if 'entity_id' in atts_required:
            output_dict['entity_id']= np.array_equal(dict_A['entity_id'], dict_B['entity_id'])

        if 'entity_name' in atts_required:
            output_dict['entity_name']= np.array_equal(dict_A['entity_name'], dict_B['entity_name'])

        if 'entity_type' in atts_required:
            output_dict['entity_type']= np.array_equal(dict_A['entity_type'], dict_B['entity_type'])

        atts = atts_required & set(['n_bonds', 'bond_index', 'bond_id', 'bond_order', 'bond_type',
            'bonded_atom_pairs'])

        if len(atts)>0:

            if 'bonded_atom_pairs' not in atts:

                atom_pairs_A = get(molecular_system, element='bond', selection=selection,
                                     syntax=syntax, bonded_atom_pairs=True)
                atom_pairs_B = get(molecular_system_2, element='bond', selection=selection_2,
                        syntax=syntax, bonded_atom_pairs=True)

            else:

                atom_pairs_A = dict_A['bonded_atom_pairs']
                atom_pairs_B = dict_B['bonded_atom_pairs']

            atom_pairs_A = np.array(atom_pairs_A)
            atom_pairs_B = np.array(atom_pairs_B)

            order_in_A = np.lexsort((atom_pairs_A[:, 1], atom_pairs_A[:, 0])).tolist()
            order_in_B = np.lexsort((atom_pairs_B[:, 1], atom_pairs_B[:, 0])).tolist()

            if 'n_bonds' in atts:
                output_dict['n_bonds']= (dict_A['n_bonds']==dict_B['n_bonds'])

            if 'bond_index' in atts:
                tmp_A = [dict_A['bond_index'][ii] for ii in order_in_A]
                tmp_B = [dict_B['bond_index'][ii] for ii in order_in_B]
                output_dict['bond_index']= np.array_equal(tmp_A, tmp_B)
                del tmp_A, tmp_B

            if 'bond_id' in atts:
                tmp_A = [dict_A['bond_id'][ii] for ii in order_in_A]
                tmp_B = [dict_B['bond_id'][ii] for ii in order_in_B]
                output_dict['bond_id']= np.array_equal(tmp_A, tmp_B)
                del tmp_A, tmp_B

            if 'bond_order' in atts:
                if (dict_A['bond_order'] is not None) and (dict_B['bond_order'] is not None):
                    tmp_A = [dict_A['bond_order'][ii] for ii in order_in_A]
                    tmp_B = [dict_B['bond_order'][ii] for ii in order_in_B]
                    output_dict['bond_order']= np.array_equal(tmp_A, tmp_B)
                    del tmp_A, tmp_B
                elif (dict_A['bond_order'] is None) and (dict_B['bond_order'] is None):
                    output_dict['bond_order'] = True
                else:
                    output_dict['bond_order'] = False

            if 'bond_type' in atts:
                if (dict_A['bond_type'] is not None) and (dict_B['bond_type'] is not None):
                    tmp_A = [dict_A['bond_type'][ii] for ii in order_in_A]
                    tmp_B = [dict_B['bond_type'][ii] for ii in order_in_B]
                    output_dict['bond_type']= np.array_equal(tmp_A, tmp_B)
                    del tmp_A, tmp_B
                elif (dict_A['bond_type'] is None) and (dict_B['bond_type'] is None):
                    output_dict['bond_type'] = True
                else:
                    output_dict['bond_type'] = False

            if 'bonded_atom_pairs' in atts:
                tmp_A = [dict_A['bonded_atom_pairs'][ii] for ii in order_in_A]
                tmp_B = [dict_B['bonded_atom_pairs'][ii] for ii in order_in_B]
                output_dict['bonded_atom_pairs']= np.array_equal(tmp_A, tmp_B)
                del tmp_A, tmp_B

            del(order_in_A, order_in_B, atom_pairs_A, atom_pairs_B)

        atts = atts_required & set(['inner_bonded_atom_pairs', 'inner_bond_index', 'n_inner_bonds'])

        if len(atts)>0:

            if 'inner_bonded_atom_pairs' not in atts:

                atom_pairs_A = get(molecular_system, element='atom', selection=selection,
                                     syntax=syntax, inner_bonded_atom_pairs=True)
                atom_pairs_B = get(molecular_system_2, element='atom', selection=selection_2,
                        syntax=syntax, inner_bonded_atom_pairs=True)

            else:

                atom_pairs_A = dict_A['inner_bonded_atom_pairs']
                atom_pairs_B = dict_B['inner_bonded_atom_pairs']

            atom_pairs_A = np.array(atom_pairs_A)
            atom_pairs_B = np.array(atom_pairs_B)
            order_in_A = np.lexsort((atom_pairs_A[:, 1], atom_pairs_A[:, 0])).tolist()
            order_in_B = np.lexsort((atom_pairs_B[:, 1], atom_pairs_B[:, 0])).tolist()

            if 'n_inner_bonds' in atts:
                output_dict['n_inner_bonds']= (dict_A['n_inner_bonds'] == dict_B['n_inner_bonds'])

            if 'inner_bond_index' in atts:
                if len(dict_A['inner_bond_index'])==len(dict_B['inner_bond_index']):
                    aux = [ii==jj for ii,jj in zip(dict_A['inner_bond_index'], dict_B['inner_bond_index'])]
                    output_dict['inner_bond_index']= all(aux)
                else:
                    output_dict['inner_bond_index']= False


            if 'inner_bonded_atom_pairs' in atts:
                tmp_A = [dict_A['inner_bonded_atom_pairs'][ii] for ii in order_in_A]
                tmp_B = [dict_B['inner_bonded_atom_pairs'][ii] for ii in order_in_B]
                output_dict['inner_bonded_atom_pairs']= np.array_equal(tmp_A, tmp_B)

        ## n_structures, structure_index, structure_id, coordinates, velocities, box

        if 'n_structures' in atts_required:
            output_dict['n_structures']= (dict_A['n_structures']==dict_B['n_structures'])

        if 'structure_index' in atts_required:
            output_dict['structure_index']= np.array_equal(dict_A['structure_index'], dict_B['structure_index'])

        if 'structure_id' in atts_required:
            output_dict['structure_id']= np.array_equal(dict_A['structure_id'], dict_B['structure_id'])

        if 'coordinates' in atts_required:
            
            if dict_A['coordinates'] is None:
                if dict_B['coordinates'] is None:
                    output_dict['coordinates']=True
                else:
                    output_dict['coordinates']=False
            else:
                if dict_B['coordinates'] is None:
                    output_dict['coordinates']=False
                else:
                    if dict_A['coordinates'].shape == dict_B['coordinates'].shape:
                        output_dict['coordinates'] = np.allclose(dict_A['coordinates'], dict_B['coordinates'])
                    else:
                        output_dict['coordinates'] = False

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
                    if dict_A['velocities'].shape == dict_B['velocities'].shape:
                        output_dict['velocities'] = np.allclose(dict_A['velocities'], dict_B['velocities'])
                    else:
                        output_dict['velocities'] = False

        if 'box' in atts_required:

            output_dict['box']= np.allclose(dict_A['box'], dict_B['box'], rtol=1e-04, atol=1e-06)

        if 'box_shape' in atts_required:
            output_dict['box_shape']= (dict_A['box_shape']==dict_B['box_shape'])

        if 'box_volume' in atts:
            output_dict['box_volume']=(dict_A['box_volume']==dict_B['box_volume'])

        if 'box_lengths' in atts:
            output_dict['box_lengths']=np.allclose(dict_A['box_lengths'], dict_B['box_lengths'])

        if 'box_angles' in atts:
            output_dict['box_angles']=np.allclose(dict_A['box_angles'], dict_B['box_angles'])


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

