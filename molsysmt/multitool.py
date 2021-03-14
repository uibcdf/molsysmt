import numpy as np
from molsysmt import puw
from molsysmt.forms import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.selection import selection_is_all
from molsysmt._private_tools.forms import to_form_is_file, form_of_file, are_equal_sets_of_forms
from molsysmt._private_tools.get_arguments import where_get_argument
from molsysmt._private_tools.set_arguments import where_set_argument
from molsysmt._private_tools.elements import elements2string
from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.selection import indices_to_selection
from molsysmt._private_tools.frame_indices import complementary_frame_indices
from molsysmt._private_tools.atom_indices import complementary_atom_indices
from molsysmt.tools.molecular_systems import is_a_single_molecular_system
from molsysmt.molecular_system import MolecularSystem

####
#### Methods
####

def get_form(molecular_system):

    if type(molecular_system)==MolecularSystem:
        _, output = molecular_system.get_items()
        output = digest_output(output)
        return output

    if puw.is_quantity(molecular_system):

        from .forms.classes.api_XYZ import this_Quantity_is_XYZ
        if this_Quantity_is_XYZ(molecular_system):
            return 'XYZ'
        else:
            raise NotImplementedError()

    if type(molecular_system)==str:

        if ':' in molecular_system:
            prefix=molecular_system.split(':')[0]
            if prefix+':id' in dict_is_form.keys():
                molecular_system=dict_is_form[prefix+':id']
            elif prefix+':seq' in dict_is_form.keys():
                molecular_system=dict_is_form[prefix+':seq']
        else:
            molecular_system=molecular_system.split('.')[-1]

    if is_list_or_tuple(molecular_system):
        output = [get_form(ii) for ii in molecular_system]
        return output

    try:
        return dict_is_form[type(molecular_system)]
    except:
        try:
            return dict_is_form[molecular_system]
        except:
            raise NotImplementedError()


def select(molecular_system, selection='all', target='atom', mask=None, syntaxis='MolSysMT', to_syntaxis=None):

    # to_syntaxis: 'NGLView', 'MDTraj', ...

    """select(item, selection='all', target='atom', syntaxis='MolSysMT')

    Get the atom indices corresponding to a selection criterion.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form (see: :doc:`/Forms`). The object being acted on by the method.

    selection: str, default='all'
       Selection criterion given by means of a string following any of the selection syntaxis parsable by MolSysMT.

    mask: list, tuple, numpy array or None. default=None
       XXX

    target: str, default='atom'
       The output indices list can correspond to 'atom', 'group', 'component', 'molecule', 'chain',
       'entity' or 'bond' indices.

    syntaxis: str, default='MolSysMT'
       Syntaxis used to write the argument `selection`. The current options supported by MolSysMt
       can be found in :doc:`/Atoms_Selection`.

    Returns
    -------

    Numpy array of integers
        List of indices in agreement with the selection criterion applied over `item`. The nature
        of the indices is chosen with the input argument 'output_indices': 'atom' (default),
        'group', 'component', 'molecule', 'chain' or 'entity'.

    Examples
    --------

    :doc:`/Atoms_Selection`

    See Also
    --------

    Notes
    -----

    """

    molecular_system = digest_molecular_system(molecular_system)

    target = digest_target(target)
    syntaxis = digest_syntaxis(syntaxis)
    selection = digest_selection(selection, syntaxis)
    to_syntaxis = digest_to_syntaxis(to_syntaxis)

    if mask is 'all':
        mask=None

    if type(selection)==str:
        if selection in ['all', 'All', 'ALL']:
            n_atoms = get(molecular_system, target='system', n_atoms=True)
            atom_indices = np.arange(n_atoms, dtype='int64')
        else:
            selection = digest_selection(selection, syntaxis)
            atom_indices = dict_select[molecular_system.elements_form][syntaxis](molecular_system.elements_item, selection)
    elif type(selection) in [int, np.int64, np.int]:
        atom_indices = np.array([selection], dtype='int64')
    elif hasattr(selection, '__iter__'):
        atom_indices = np.array(selection, dtype='int64')
    else :
        atom_indices = None

    output_indices = []

    if target=='atom':
        output_indices = atom_indices
    elif target=='group':
        output_indices = get(molecular_system, target='atom', indices=atom_indices, group_index=True)
        output_indices = np.unique(output_indices)
    elif target=='component':
        output_indices = get(molecular_system, target='atom', indices=atom_indices, component_index=True)
        output_indices = np.unique(output_indices)
    elif target=='chain':
        output_indices = get(molecular_system, target='atom', indices=atom_indices, chain_index=True)
        output_indices = np.unique(output_indices)
    elif target=='molecule':
        output_indices = get(molecular_system, target='atom', indices=atom_indices, molecule_index=True)
        output_indices = np.unique(output_indices)
    elif target=='entity':
        output_indices = get(molecular_system, target='atom', indices=atom_indices, entity_index=True)
        output_indices = np.unique(output_indices)
    elif target=='bond':
        output_indices = get(molecular_system, target='atom', indices=atom_indices, inner_bond_index=True)

    else:
        raise NotImplementedError()

    if mask is not None:
        output_indices = np.intersect1d(output_indices, mask, assume_unique=True)

    if to_syntaxis is None:
        return output_indices
    else:
        return indices_to_selection(molecular_system, output_indices, target=target, syntaxis=to_syntaxis)


def get(molecular_system, target='atom', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

    """get(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT')

    Get specific attributes and observables.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).


    selection: str, list, tuple or np.ndarray, default='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT.

    syntaxis: str, default='MolSysMT'
       Selection syntaxis used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolSysMt in section 'Selection'.

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        chosen.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    """

    molecular_system = digest_molecular_system(molecular_system)

    # selection works as a mask if indices or ids are used

    target = digest_target(target)
    attributes = [ digest_get_argument(key, target) for key in kwargs.keys() if kwargs[key] ]
    indices = digest_indices(indices)
    frame_indices = digest_frame_indices(frame_indices)

    # doing the work here

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, target=target, selection=selection, syntaxis=syntaxis)
        else:
            indices = 'all'

    output = []
    for attribute in attributes:

        result = None

        for where_attribute in where_get_argument[attribute]:
            item = getattr(molecular_system, where_attribute+'_item')
            form = getattr(molecular_system, where_attribute+'_form')

            if item is not None:
                result = dict_get[form][target][attribute](item, indices=indices, frame_indices=frame_indices)
            if result is not None:
                break

        output.append(result)

    output=digest_output(output)
    return output

def remove(molecular_system, selection=None, frame_indices=None, to_form=None, syntaxis='MolSysMT'):

    """remove(item, selection=None, frame_indices=None, syntaxis='MolSysMT')

    Remove atoms or frames from the molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    selection: str, list, tuple or np.ndarray, default=None
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    frame_indices: str, list, tuple or np.ndarray, default=None
        XXX

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    item: molecular model
        The result is a new molecular model with the same form as the input item.

    Examples
    --------
    Remove chains 0 and 1 from the pdb: 1B3T.
    >>> import molsysmt as m3t
    >>> system = m3t.load('pdb:1B3T')
    Check the number of chains
    >>> m3t.get(system, n_chains=True)
    8
    Remove chains 0 and 1
    >>> new_system = m3t.remove(system, 'chainid 0 1')
    Check the number of chains of the new molecular model
    >>> m3t.get(new_system, n_chains=True)
    6

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----
    There is a specific method to remove solvent atoms: molsysmt.remove_solvent and another one to
    remove hydrogens: molsysmt.remove_hydrogens.

    """

    molecular_system = digest_molecular_system(molecular_system)
    frame_indices = digest_frame_indices(frame_indices)

    atom_indices_to_be_kept = 'all'
    frame_indices_to_be_kept = 'all'

    if selection is not None:
        atom_indices_to_be_removed = select(molecular_system, selection=selection, syntaxis=syntaxis)
        atom_indices_to_be_kept = complementary_atom_indices(molecular_system, atom_indices_to_be_removed)

    if frame_indices is not None:
        frame_indices_to_be_kept = complementary_frame_indices(molecular_system, frame_indices)

    return extract(molecular_system, selection=atom_indices_to_be_kept, frame_indices=frame_indices_to_be_kept, to_form=to_form)


def extract(molecular_system, selection='all', frame_indices='all', to_form=None, syntaxis='MolSysMT'):

    """extract(item, selection='all', frame_indices='all', syntaxis='MolSysMT')

    Extract a subset of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----

    """

    if (selection is 'all') and (frame_indices is 'all') and (to_form is None):
        return copy(molecular_system)

    molecular_system = digest_molecular_system(molecular_system)
    items, forms = molecular_system.get_items()

    frame_indices = digest_frame_indices(frame_indices)
    to_form = digest_to_form(to_form)

    if selection is 'all':
        atom_indices='all'
    else:
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)

    tmp_items = []

    for item, form_in in zip(items, forms):
        form_in = get_form(item)
        tmp_item = dict_extract[form_in](item, atom_indices=atom_indices, frame_indices=frame_indices) # si es file debe ir a un temporal para ser renombrado luego
        tmp_items.append(tmp_item)

    if to_form is None:
        return tmp_items
    else:
        tmp_items = convert(tmp_items, to_form=to_form)

    return tmp_items

def add(to_molecular_system, from_molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT'):

    to_molecular_system = digest_molecular_system(to_molecular_system)

    if is_a_single_molecular_system(from_molecular_systems):
        from_molecular_systems = [digest_molecular_system(from_molecular_systems)]
    else:
        tmp_from_molecular_systems = []
        for aux in from_molecular_systems:
            tmp_from_molecular_systems.append(digest_molecular_system(aux))
        from_molecular_systems = tmp_from_molecular_systems

    n_from_molecular_systems = len(tmp_from_molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_from_molecular_systems)]
    elif len(selections)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(frame_indices):
        frame_indices = [digest_frame_indices(frame_indices) for ii in range(n_from_molecular_systems)]
    elif len(frame_indices)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and frame_indices need to be equal.")


    to_already_added=[]

    for aux_molecular_system, aux_selection, aux_frame_indices in zip(from_molecular_systems, selections, frame_indices):

        atom_indices = select(aux_molecular_system, selection=aux_selection, syntaxis=syntaxis)

        # topology

        to_form = to_molecular_system.elements_form
        to_item = to_molecular_system.elements_item

        if to_form is not None:
            from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
            dict_add[to_form](to_item, from_item)
            to_already_added.append(to_item)

        # parameters

        to_form = to_molecular_system.parameters_form
        to_item = to_molecular_system.parameters_item

        if to_form is not None:
            if to_item not in to_already_added:
                from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
                dict_add[to_form](to_item, from_item)
                to_already_added.append(to_item)

        # bonds

        to_form = to_molecular_system.bonds_form
        to_item = to_molecular_system.bonds_item

        if to_form is not None:
            if to_item not in to_already_added:
                from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
                dict_add[to_form](to_item, from_item)
                to_already_added.append(to_item)

        # coordinates

        to_form = to_molecular_system.coordinates_form
        to_item = to_molecular_system.coordinates_item

        if to_form is not None:
            if to_item not in to_already_added:
                from_item = convert(aux_molecular_system, selection=atom_indices, frame_indices=aux_frame_indices, syntaxis=syntaxis, to_form=to_form)
                dict_add[to_form](to_item, from_item)
                to_already_added.append(to_item)

        # The box info is taken from the first molecular_system

    pass

def merge(molecular_systems=None, selections='all', frame_indices='all', syntaxis='MolSysMT', to_form=None):

    """merge(items=None, selection='all', frame_indices='all', syntaxis='MolSysMT' to_form=None)

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
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`
    Notes
    -----

    """

    if is_a_single_molecular_system(molecular_systems):
        raise NeedsMultipleMolecularSystemsError()

    tmp_molecular_systems = []
    for aux in molecular_systems:
        tmp_molecular_systems.append(digest_molecular_system(aux))
    molecular_systems = tmp_molecular_systems

    n_molecular_systems = len(molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(frame_indices):
        frame_indices = [digest_frame_indices(frame_indices) for ii in range(n_molecular_systems)]
    elif len(frame_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and frame_indices need to be equal.")

    if to_form is None:
        tmp_molecular_system = extract(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0])
    else:
        tmp_molecular_system = convert(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0], to_form=to_form)

    add(tmp_molecular_system, molecular_systems[1:], selections=selections[1:], frame_indices=frame_indices[1:])

    return tmp_molecular_system

def append_frames(to_molecular_system, from_molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT'):

    to_molecular_system = digest_molecular_system(to_molecular_system)

    if is_a_single_molecular_system(from_molecular_systems):
        from_molecular_systems = [digest_molecular_system(from_molecular_systems)]
    else:
        tmp_from_molecular_systems = []
        for aux in from_molecular_systems:
            tmp_from_molecular_systems.append(digest_molecular_system(aux))
        from_molecular_systems = tmp_from_molecular_systems

    n_from_molecular_systems = len(tmp_from_molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_from_molecular_systems)]
    elif len(selections)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(frame_indices):
        frame_indices = [digest_frame_indices(frame_indices) for ii in range(n_from_molecular_systems)]
    elif len(frame_indices)!=n_from_molecular_systems:
        raise ValueError("The length of the lists items and frame_indices need to be equal.")

    box_in_diff_item=False
    if to_molecular_system.coordinates_item != to_molecular_system.box_item:
        box_in_diff_item=True

    for aux_molecular_system, aux_selection, aux_frame_indices in zip(from_molecular_systems, selections, frame_indices):

        step, time, coordinates, box = get(aux_molecular_system, target='atom', selection=aux_selection, frame_indices=aux_frame_indices, frame=True)

        if box_in_diff_item:
            dict_append_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=None)
            dict_append_frames[to_molecular_system.box_form](to_molecular_system.box_item, step=None, time=None, coordinates=None, box=box)
        else:
            dict_append_frames[to_molecular_system.coordinates_form](to_molecular_system.coordinates_item, step=step, time=time, coordinates=coordinates, box=box)

    pass

def concatenate_frames(molecular_systems, selections='all', frame_indices='all', syntaxis='MolSysMT', to_form=None):

    if is_a_single_molecular_system(molecular_systems):
        raise NeedsMultipleMolecularSystemsError()

    tmp_molecular_systems = []
    for aux in molecular_systems:
        tmp_molecular_systems.append(digest_molecular_system(aux))
    molecular_systems = tmp_molecular_systems

    n_molecular_systems = len(molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(frame_indices):
        frame_indices = [digest_frame_indices(frame_indices) for ii in range(n_molecular_systems)]
    elif len(frame_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and frame_indices need to be equal.")

    if to_form is None:
        tmp_molecular_system = extract(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0])
    else:
        tmp_molecular_system = convert(molecular_systems[0], selection=selections[0], frame_indices=frame_indices[0], to_form=to_form)

    append_frames(tmp_molecular_system, molecular_systems[1:], selections=selections[1:], frame_indices=frame_indices[1:])

    return tmp_molecular_system

def info(molecular_system, target='system', indices=None, selection='all', syntaxis='MolSysMT', output='dataframe'):

    """info(item, target='system', indices=None, selection='all', syntaxis='MolSysMT')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).


    selection: str, list, tuple or np.ndarray, default='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT.

    syntaxis: str, default='MolSysMT'
       Selection syntaxis used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolSysMt in section 'Selection'.

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    """

    molecular_system = digest_molecular_system(molecular_system)

    target = digest_target(target)

    if output=='dataframe':

        from pandas import DataFrame as df

        if target=='atom':

            atom_index, atom_id, atom_name, atom_type,\
            group_index, group_id, group_name, group_type,\
            component_index,\
            chain_index,\
            molecule_index, molecule_type,\
            entity_index, entity_name= get(molecular_system, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                           atom_index=True, atom_id=True, atom_name=True, atom_type=True,
                                           group_index=True, group_id=True, group_name=True, group_type=True,
                                           component_index=True,
                                           chain_index=True,
                                           molecule_index=True, molecule_type=True,
                                           entity_index=True, entity_name=True)

            return df({'index':atom_index, 'id':atom_id, 'name':atom_name, 'type':atom_type,
                       'group index':group_index, 'group id':group_id, 'group name':group_name, 'group type':group_type,
                       'component index':component_index,
                       'chain index':chain_index,
                       'molecule index':molecule_index, 'molecule type':molecule_type,
                       'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

        elif target=='group':

            group_index, group_id, group_name, group_type,\
            n_atoms, component_index,\
            chain_index,\
            molecule_index, molecule_type,\
            entity_index, entity_name = get(molecular_system, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                            group_index=True, group_id=True, group_name=True, group_type=True, n_atoms=True,
                                            component_index=True, chain_index=True, molecule_index=True, molecule_type=True,
                                            entity_index=True, entity_name=True)

            return df({'index':group_index, 'id':group_id, 'name':group_name, 'type':group_type,
                       'n atoms':n_atoms,
                       'component index':component_index,
                       'chain index':chain_index,
                       'molecule index':molecule_index, 'molecule type':molecule_type,
                       'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

        elif target=='component':

            component_index, n_atoms, n_groups,\
            chain_index,\
            molecule_index, molecule_type,\
            entity_index, entity_name = get(molecular_system, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                            component_index=True, n_atoms=True, n_groups=True,
                                            chain_index=True,
                                            molecule_index=True, molecule_type=True,
                                            entity_index=True, entity_name=True)

            return df({'index':component_index,
                       'n atoms':n_atoms, 'n groups':n_groups,
                       'chain index':chain_index,
                       'molecule index':molecule_index, 'molecule type':molecule_type,
                       'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

        elif target=='chain':

            chain_index, chain_id, chain_name,\
            n_atoms, n_groups, n_components,\
            molecule_index, molecule_type,\
            entity_index, entity_name = get(molecular_system, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                            chain_index=True, chain_id=True, chain_name=True,
                                            n_atoms=True, n_groups=True, n_components=True,
                                            molecule_index=True, molecule_type=True,
                                            entity_index=True, entity_name=True)

            if len(molecule_index.shape)>1:
                n_objects = molecule_index.shape[0]
                aux_obj1_array = np.empty([n_objects], dtype='object')
                aux_obj2_array = np.empty([n_objects], dtype='object')
                for ii in range(n_objects):
                    aux_obj1_array[ii]=molecule_index[ii]
                    aux_obj2_array[ii]=molecule_type[ii]
                molecule_index=aux_obj1_array
                molecule_type=aux_obj2_array

            for ii in range(len(molecule_index)):
                if len(molecule_index[ii])==1:
                    molecule_index[ii]=molecule_index[ii][0]
                    molecule_type[ii]=molecule_type[ii][0]

            if len(entity_index.shape)>1:
                n_objects =entity_index.shape[0]
                aux_obj1_array = np.empty([n_objects], dtype='object')
                aux_obj2_array = np.empty([n_objects], dtype='object')
                for ii in range(n_objects):
                    aux_obj1_array[ii]=entity_index[ii]
                    aux_obj2_array[ii]=entity_name[ii]
                entity_index=aux_obj1_array
                entity_name=aux_obj2_array

            for ii in range(len(entity_index)):
                if len(entity_index[ii])==1:
                    entity_index[ii]=entity_index[ii][0]
                    entity_name[ii]=entity_name[ii][0]

            return df({'index':chain_index, 'id':chain_id, 'name':chain_name,
                       'n atoms':n_atoms, 'n groups':n_groups, 'n components':n_components,
                       'molecule index':molecule_index, 'molecule type':molecule_type,
                       'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

        elif target=='molecule':

            molecule_index, molecule_name, molecule_type,\
            n_atoms, n_groups, n_components, chain_index,\
            entity_index, entity_name = get(molecular_system, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                            molecule_index=True, molecule_name=True, molecule_type=True,
                                            n_atoms=True, n_groups=True, n_components=True, chain_index=True,
                                            entity_index=True, entity_name=True)

            if len(chain_index.shape)>1:
                n_objects = chain_index.shape[0]
                aux_obj_array = np.empty([n_objects], dtype='object')
                for ii in range(n_objects):
                    aux_obj_array[ii]=chain_index[ii]
                chain_index=aux_obj_array

            for ii in range(len(chain_index)):
                if len(chain_index[ii])==1:
                    chain_index[ii]=chain_index[ii][0]

            return df({'index':molecule_index, 'name':molecule_name, 'type':molecule_type,
                       'n atoms':n_atoms, 'n groups':n_groups, 'n components':n_components,
                       'chain index':chain_index,
                       'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

        elif target=='entity':

            entity_index, entity_name, entity_type,\
            n_atoms, n_groups, n_components, n_chains,\
            n_molecules = get(molecular_system, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                    entity_index=True, entity_name=True, entity_type=True,
                    n_atoms=True, n_groups=True, n_components=True,
                    n_chains=True, n_molecules=True)

            return df({'index':entity_index, 'name':entity_name, 'type': entity_type,
                       'n atoms':n_atoms, 'n groups':n_groups, 'n components':n_components,
                       'n chains':n_chains, 'n molecules':n_molecules
                       }).style.hide_index()

        elif target=='system':

            form = get_form(molecular_system)

            n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities, n_frames,\
            n_ions, n_waters, n_cosolutes, n_small_molecules, n_peptides, n_proteins, n_dnas,\
            n_rnas = get(molecular_system, target=target,
                    n_atoms=True, n_groups=True, n_components=True, n_chains=True, n_molecules=True, n_entities=True, n_frames=True,
                    n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True, n_peptides=True, n_proteins=True,
                    n_dnas=True, n_rnas=True)

            tmp_df = df([{'form':form, 'n_atoms':n_atoms, 'n_groups':n_groups, 'n_components':n_components,
                'n_chains':n_chains, 'n_molecules':n_molecules, 'n_entities':n_entities,
                'n_waters':n_waters, 'n_ions':n_ions, 'n_cosolutes':n_cosolutes, 'n_small_molecules':n_small_molecules,
                'n_peptides':n_peptides, 'n_proteins':n_proteins, 'n_dnas':n_dnas, 'n_rnas':n_rnas,
                'n_frames':n_frames}], index=[0])

            if n_ions==0 or n_ions is None: tmp_df.drop(columns=['n_ions'], inplace=True)
            if n_waters==0 or n_waters is None: tmp_df.drop(columns=['n_waters'], inplace=True)
            if n_cosolutes==0 or n_cosolutes is None: tmp_df.drop(columns=['n_cosolutes'], inplace=True)
            if n_small_molecules==0 or n_small_molecules is None: tmp_df.drop(columns=['n_small_molecules'], inplace=True)
            if n_peptides==0 or n_peptides is None: tmp_df.drop(columns=['n_peptides'], inplace=True)
            if n_proteins==0 or n_proteins is None: tmp_df.drop(columns=['n_proteins'], inplace=True)
            if n_dnas==0 or n_dnas is None: tmp_df.drop(columns=['n_dnas'], inplace=True)
            if n_rnas==0 or n_rnas is None: tmp_df.drop(columns=['n_rnas'], inplace=True)

            return tmp_df.style.hide_index()

        else:

            raise ValueError('"target" needs one of the following strings: "atom", "group",\
                             "component", "chain", "molecule", "entity" or "system"')

    elif output=='short_string':

        string = None

        if indices is None and selection is not None:

            indices = select(molecular_system, selection=selection, target=target)

        string = elements2string(molecular_system, indices=indices, target=target)

        if len(string)==1:
            return string[0]
        else:
            return string

    elif output=='long_string':

        if target=='atom':

            group_indices, chain_indices, molecule_indices = get(molecular_system, target=target, indices=indices, group_index=True,
                                chain_index=True, molecule_index=True)

            atom_string = elements2string(molecular_system, indices=indices, target=target)
            group_string = elements2string(molecular_system, indices=group_indices, target='group')
            chain_string = elements2string(molecular_system, indices=chain_indices, target='chain')
            molecule_string = elements2string(molecular_system, indices=molecule_indices, target='molecule')

            string=[]

            for list_strings in zip(atom_string, group_string, chain_string,
                                    molecule_string):

                string.append('/'.join(list_strings))

            if len(string)==1:
                string=string[0]

        elif target=='group':

            chain_indices, molecule_indices = get(molecular_system, target=target, indices=indices,
                                chain_index=True, molecule_index=True)

            group_string = elements2string(molecular_system, indices=indices, target=target)
            chain_string = elements2string(molecular_system, indices=chain_indices, target='chain')
            molecule_string = elements2string(molecular_system, indices=molecule_indices, target='molecule')

            string=[]

            for list_strings in zip(group_string, chain_string,
                                    molecule_string):

                string.append('/'.join(list_strings))

            if len(string)==1:
                string=string[0]

        elif target=='component':

            chain_indices, molecule_indices = get(molecular_system, target=target, indices=indices,
                                chain_index=True, molecule_index=True)

            component_string = elements2string(molecular_system, indices=indices, target=target)
            chain_string = elements2string(molecular_system, indices=chain_indices, target='chain')
            molecule_string = elements2string(molecular_system, indices=molecule_indices, target='molecule')

            string=[]

            for list_strings in zip(component_string, chain_string, molecule_string):

                string.append('/'.join(list_strings))

            if len(string)==1:
                string=string[0]

        elif target=='chain':


            chain_string = elements2string(molecular_system, indices=indices, target=target)
            string=chain_string

            if len(string)==1:
                string=string[0]

        elif target=='molecule':


            molecule_string = elements2string(molecular_system, indices=indices, target=target)
            string=molecule_string

            if len(string)==1:
                string=string[0]

        elif target=='entity':

            entity_string = elements2string(molecular_system, indices=indices, target=target)
            string=entity_string

            if len(string)==1:
                string=string[0]

        else:

            raise NotImplementedError

        return string

    else:

        raise ValueError()


def set(molecular_system, target='system', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

    """into(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT')

    Set a new value to an attribute.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    frame_indices: int, list, tuple, np.ndarray or 'all', default='all'
        List of indices referring the set of frames this method is going to work with. This set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------

    None
        XXX.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----

    """

    molecular_system = digest_molecular_system(molecular_system)

    # selection works as a mask if indices or ids are used

    target = digest_target(target)
    value_of_attribute = { digest_set_argument(key, target): kwargs[key] for key in kwargs.keys()}
    attributes = value_of_attribute.keys()
    indices = digest_indices(indices)
    frame_indices = digest_frame_indices(frame_indices)

    # doing the work here

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, target=target, selection=selection, syntaxis=syntaxis)
        else:
            indices = 'all'

    for attribute in attributes:

        for where_attribute in where_set_argument[attribute]:
            item = getattr(molecular_system, where_attribute+'_item')
            form = getattr(molecular_system, where_attribute+'_form')

            if item is not None:
                value = value_of_attribute[attribute]
                dict_set[form][target][attribute](item, indices=indices, frame_indices=frame_indices, value=value)

    pass

def convert(molecular_system, to_form='molsysmt.MolSys', selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

    """convert(item, to_form='molsysmt.MolSys', selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs)

    Convert a molecular model into other form.

    A molecular model in a given accepted form can be converted into any other supported form
    by MolSysMt. The list of supported forms can be found in the section 'XXX'.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form by MolSysMT (see: XXX).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    to_form: str, default='molsysmt.MolSys'
        The output object will take the form specified here. This form supported form by MolSysMt
        for the output object.

    syntaxis: str, default='MolSysMT'
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

    :func:`molsysmt.load`, :func:`molsysmt.select`

    Notes
    -----

    """

    molecular_system = digest_molecular_system(molecular_system)
    _, forms_in = molecular_system.get_items()

    if are_equal_sets_of_forms(forms_in,to_form):
        if (selection is 'all') and (frame_indices is 'all'):
            return copy(molecular_system)
        else:
            return extract(molecular_system, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    to_form = digest_to_form(to_form)

    if is_list_or_tuple(to_form):

        tmp_item=[]
        for item_out in to_form:
            tmp_item.append(convert(molecular_system, to_form=item_out, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis))

        return tmp_item

    frame_indices = digest_frame_indices(frame_indices)

    if not selection_is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
    else:
        atom_indices = 'all'

    tmp_item = None
    form_out = None
    conversion_arguments={}

    if to_form_is_file(to_form):
        conversion_arguments['output_filename'] = to_form
        form_out = form_of_file(to_form)
    else:
        form_out = to_form

    item = None
    item_form = None

    if molecular_system.elements_item is not None:
        if form_out in dict_convert[molecular_system.elements_form]:
            item = molecular_system.elements_item
            item_form = molecular_system.elements_form

    if item is None:
        if molecular_system.coordinates_item is not None:
            if form_out in dict_convert[molecular_system.coordinates_form]:
                item = molecular_system.coordinates_item
                item_form = molecular_system.coordinates_form

    if item is None:
        if molecular_system.box_item is not None:
            if form_out in dict_convert[molecular_system.box_form]:
                item = molecular_system.box_item
                item_form = molecular_system.box_form

    if item is None:
        if molecular_system.velocities_item is not None:
            if form_out in dict_convert[molecular_system.velocities_form]:
                item = molecular_system.velocities_item
                item_form = molecular_system.velocities_form

    if item is None:
        if molecular_system.bonds_item is not None:
            if form_out in dict_convert[molecular_system.bonds_form]:
                item = molecular_system.bonds_item
                item_form = molecular_system.bonds_form

    if item is None:
        if molecular_system.ff_parameters_item is not None:
            if form_out in dict_convert[molecular_system.ff_parameters_form]:
                item = molecular_system.ff_parameters_item
                item_form = molecular_system.ff_parameters_form

    if item is None:
        if molecular_system.mm_parameters_item is not None:
            if form_out in dict_convert[molecular_system.mm_parameters_form]:
                item = molecular_system.mm_parameters_item
                item_form = molecular_system.mm_parameters_form

    if item is None:
        if molecular_system.simulation is not None:
            if form_out in dict_convert[molecular_system.simulation_form]:
                item = molecular_system.simulation_item
                item_form = molecular_system.simulation_form

    if item_form!=form_out:

        tmp_item = dict_convert[item_form][form_out](item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices,
                                                     **conversion_arguments, **kwargs)
    else:

        tmp_item = extract(molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, to_form=to_form, syntaxis=syntaxis)

    return tmp_item

def copy(molecular_system, output_filename=None):

    output = []

    molecular_system = digest_molecular_system(molecular_system)
    items, forms = molecular_system.get_items()

    if output_filename is None:

        for item, form_in in zip(items, forms):
            tmp_item = dict_copy[form_in](item)
            output.append(tmp_item)

    else:

        if not is_list_or_tuple(output_filename):
            output_filename = [output_filename]
        for item, form_in, aux_filename in zip(items, forms, output_filename):
            tmp_item = dict_copy[form_in](item, output_filename=aux_filename)
            output.append(tmp_item)

    output = digest_output(output)

    return output

def view(molecular_system=None, viewer='NGLView', selection='all', frame_indices='all',
         concatenate_frames=False, standardize=True, surface=False, syntaxis='MolSysMT'):

    viewer, form_viewer = digest_viewer(viewer)

    if is_a_single_molecular_system(molecular_system):
        molecular_system = digest_molecular_system(molecular_system)
        tmp_item = convert(molecular_system, to_form=form_viewer, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)
    else:
        if concatenate_frames:
            molecular_system = concatenate_frames(molecular_system, selections=selection, frame_indices=frame_indices, syntaxis=syntaxis)
        else:
            molecular_system = merge(molecular_system, selections=selection, frame_indices=frame_indices, syntaxis=syntaxis)
        tmp_item = convert(molecular_system, to_form=form_viewer)

    if standardize:
        if viewer=='NGLView':
            from molsysmt.tools.nglview import standardize_view
            standardize_view(tmp_item)

    if surface:
        if viewer=='NGLView':
            from molsysmt.tools.nglview import show_system_as_transparent_surface
            show_system_as_transparent_surface(tmp_item)

    return tmp_item

