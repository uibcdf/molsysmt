import os
import tempfile
from .utils.exceptions import *
from .utils.arguments import singular as _singular
from .utils.forms import digest as _digest_forms
from .utils.frame_indices import digest as _digest_frame_indices
from .utils.selection import digest as _digest_selection
from .utils.atom_indices import intersection_indices as _intersection_indices
from numpy import unique as _unique
from numpy import ndarray as _ndarray
from numpy import array as _array
from numpy import empty as _empty
from numpy import sort as _sort
from numpy import arange as _arange
from numpy import int as _int
from numpy import int64 as _int64

####
#### Molecular Models forms
####

# Classes
from .forms.classes import dict_is_form as _dict_classes_is_form, \
    list_forms as _list_classes_forms, \
    dict_info as _dict_classes_infotxt, \
    dict_converter as _dict_classes_converter, \
    dict_selector as _dict_classes_selector, \
    dict_extractor as _dict_classes_extractor, \
    dict_duplicator as _dict_classes_duplicator, \
    dict_merger as _dict_classes_merger, \
    dict_get as _dict_classes_get, \
    dict_set as _dict_classes_set

# Files
from .forms.files import dict_is_form as _dict_files_is_form, \
    list_forms as _list_files_forms, \
    dict_info as _dict_files_infotxt, \
    dict_converter as _dict_files_converter, \
    dict_selector as _dict_files_selector, \
    dict_extractor as _dict_files_extractor, \
    dict_duplicator as _dict_files_duplicator, \
    dict_merger as _dict_files_merger, \
    dict_get as _dict_files_get, \
    dict_set as _dict_files_set

# IDs
from .forms.ids import dict_is_form as _dict_ids_is_form, \
    list_forms as _list_ids_forms, \
    dict_info as _dict_ids_infotxt, \
    dict_converter as _dict_ids_converter, \
    dict_selector as _dict_ids_selector, \
    dict_extractor as _dict_ids_extractor, \
    dict_duplicator as _dict_ids_duplicator, \
    dict_merger as _dict_ids_merger, \
    dict_get as _dict_ids_get, \
    dict_set as _dict_ids_set

# Sequences
from .forms.seqs import dict_is_form as _dict_seqs_is_form, \
    list_forms as _list_seqs_forms, \
    dict_info as _dict_seqs_infotxt, \
    dict_converter as _dict_seqs_converter, \
    dict_selector as _dict_seqs_selector, \
    dict_extractor as _dict_seqs_extractor, \
    dict_duplicator as _dict_seqs_duplicator, \
    dict_merger as _dict_seqs_merger, \
    dict_get as _dict_seqs_get, \
    dict_set as _dict_seqs_set

# Viewers
from .forms.viewers import dict_is_form as _dict_viewers_is_form, \
    list_forms as _list_viewers_forms, \
    dict_info as _dict_viewers_infotxt, \
    dict_converter as _dict_viewers_converter, \
    dict_selector as _dict_viewers_selector, \
    dict_extractor as _dict_viewers_extractor, \
    dict_duplicator as _dict_viewers_duplicator, \
    dict_merger as _dict_viewers_merger, \
    dict_get as _dict_viewers_get, \
    dict_set as _dict_viewers_set

_dict_is_form = {**_dict_classes_is_form, **_dict_files_is_form,\
                 **_dict_ids_is_form, **_dict_seqs_is_form, **_dict_viewers_is_form}
_dict_infotxt = {**_dict_classes_infotxt, **_dict_files_infotxt,\
                   **_dict_ids_infotxt, **_dict_seqs_infotxt, **_dict_viewers_infotxt}
_dict_converter = {**_dict_classes_converter, **_dict_files_converter,\
                   **_dict_ids_converter, **_dict_seqs_converter, **_dict_viewers_converter}
_dict_selector = {**_dict_classes_selector, **_dict_files_selector,\
                   **_dict_ids_selector, **_dict_seqs_selector, **_dict_viewers_selector}
_dict_extractor = {**_dict_classes_extractor, **_dict_files_extractor,\
                   **_dict_ids_extractor, **_dict_seqs_extractor, **_dict_viewers_extractor}
_dict_duplicator = {**_dict_classes_duplicator, **_dict_files_duplicator,\
                   **_dict_ids_duplicator, **_dict_seqs_duplicator, **_dict_viewers_duplicator}
_dict_merger    = {**_dict_classes_merger, **_dict_files_merger,\
                   **_dict_ids_merger, **_dict_seqs_merger, **_dict_viewers_merger}
_dict_get = {**_dict_classes_get, **_dict_files_get,\
                   **_dict_ids_get, **_dict_seqs_get, **_dict_viewers_get}
_dict_set = {**_dict_classes_set, **_dict_files_set,\
                   **_dict_ids_set, **_dict_seqs_set, **_dict_viewers_set}

_dict_type = {}
for form in _list_classes_forms:
    _dict_type[form]='class'
for form in _list_files_forms:
    _dict_type[form]='file'
for form in _list_ids_forms:
    _dict_type[form]='id'
for form in _list_seqs_forms:
    _dict_type[form]='seq'
for form in _list_viewers_forms:
    _dict_type[form]='viewer'

_list_types = ['class', 'file', 'id', 'seq', 'viewer']

####
#### Methods
####

def select(item, selection='all', target='atom', mask=None, syntaxis='MolSysMT'):

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
       The output indices list can correspond to 'atom', 'group', 'component', 'molecule', 'chain' or 'entity'
       indices.

    syntaxis: str, default='MolSysMT'
       Syntaxis used to write the argument `selection`. The current options supported by MolSysMt
       can be found in :doc:`/Atoms_Selection`.

    Returns
    -------

    Numpy array of integers
        List of indices in agreement with the selection criterion applied over `item`. The nature
        of the indices is chosen with the impot argument 'output_indices': 'atom' (default),
        'group', 'component', 'molecule', 'chain' or 'entity'.

    Examples
    --------

    :doc:`/Atoms_Selection`

    See Also
    --------

    Notes
    -----

    """

    form_in, _ = _digest_forms(item)

    if type(selection)==str:
        if selection in ['all', 'All', 'ALL']:
            n_atoms = _dict_get[form_in]['system']['n_atoms'](item)
            atom_indices = _arange(n_atoms, dtype='int64')
        else:
            selection, syntaxis = _digest_selection(selection, syntaxis)
            atom_indices = _dict_selector[form_in][syntaxis](item, selection)
    elif type(selection) in [int, _int64, _int]:
        atom_indices = _array([selection], dtype='int64')
    elif hasattr(selection, '__iter__'):
        atom_indices = _array(selection, dtype='int64')
    else :
        atom_indices = None

    output_indices = []

    if target=='atom':
        output_indices = atom_indices
    elif target=='group':
        output_indices = get(item, target='atom', indices=atom_indices, group_index=True)
        output_indices = _unique(output_indices)
    elif target=='component':
        output_indices = get(item, target='atom', indices=atom_indices, component_index=True)
        output_indices = _unique(output_indices)
    elif target=='chain':
        output_indices = get(item, target='atom', indices=atom_indices, chain_index=True)
        output_indices = _unique(output_indices)
    elif target=='molecule':
        output_indices = get(item, target='atom', indices=atom_indices, molecule_index=True)
        output_indices = _unique(output_indices)
    elif target=='entity':
        output_indices = get(item, target='atom', indices=atom_indices, entity_index=True)
        output_indices = _unique(output_indices)

    else:
        raise NotImplementedError

    if mask is not None:
        output_indices = _intersection_indices(output_indices,mask)

    return output_indices

def remove(item, selection=None, frame_indices=None, syntaxis='MolSysMT'):

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

    atom_indices_to_be_kept = 'all'
    frame_indices_to_be_kept = 'all'

    if selection is not None:
        from .utils.atom_indices import complementary_atom_indices
        atom_indices_to_be_removed = select(item, selection, syntaxis=syntaxis)
        atom_indices_to_be_kept = complementary_atom_indices(item, atom_indices_to_be_removed)

    if frame_indices is not None:
        raise NotImplementedError("Removing frames is not implemented yet")

    return extract(item, selection=selection_to_be_kept, frame_indices=frame_indices_to_be_kept, syntaxis=syntaxis)

def extract(item, selection='all', frame_indices='all', to_form=None, syntaxis='MolSysMT'):

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

    form_in, form_out = _digest_forms(item, to_form)

    if selection is 'all':
        atom_indices='all'
    else:
        atom_indices = select(item=item, selection=selection, syntaxis=syntaxis)

    tmp_item = _dict_extractor[form_in](item, atom_indices=atom_indices, frame_indices=frame_indices)

    if form_in!=form_out:
        tmp_item = convert(tmp_item, to_form=form_out)

    return tmp_item

def merge(item1=None, item2=None, to_form=None):

    """merge(item1=None, item2=None, to_form=None)

    XXX

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    to_form: str, default='molsysmt.MolSys'
        Any accepted form by MolSysMt for the output object.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

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

    #item1 can be a list or tuple

    if type(item1) in [list,tuple]:
        _ , form_out = _digest_forms(item1[0], to_form)
        tmp_item = convert(item1[0], to_form=form_out)
        for in_item in item1[1:]:
            tmp_item2 = convert(in_item, to_form=form_out)
            tmp_item = _dict_merger[form](tmp_item, tmp_item2)
        return tmp_item
    else:
        _ , form_out = _digest_forms(item1, to_form)
        tmp_item1 = convert(item1,to_form=form)
        tmp_item2 = convert(item2,to_form=form)
        return _dict_merger[form](tmp_item1, tmp_item1)

def info(item=None, target='system', indices=None, selection='all', syntaxis='MolSysMT'):

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

    # Patch to keep "residue":
    if target=='residue':
        target='group'

    from pandas import DataFrame as df
    form_in, _ = _digest_forms(item)
    target = _singular(target)

    if target=='atom':

        atom_index, atom_id, atom_name, atom_type,\
        group_index, group_id, group_name, group_type,\
        component_index,\
        chain_index,\
        molecule_index, molecule_type,\
        entity_index, entity_name= get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
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
        component_index,\
        chain_index,\
        molecule_index, molecule_type,\
        entity_index, entity_name = get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                        group_index=True, group_id=True, group_name=True, group_type=True,
                                        component_index=True,
                                        chain_index=True,
                                        molecule_index=True, molecule_type=True,
                                        entity_index=True, entity_name=True)

        n_atoms = [ get(item, target=target, indices=index, n_atoms=True) for index in group_index ]

        return df({'index':group_index, 'id':group_id, 'name':group_name, 'type':group_type,
                   'n atoms':n_atoms,
                   'component index':component_index,
                   'chain index':chain_index,
                   'molecule index':molecule_index, 'molecule type':molecule_type,
                   'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

    elif target=='component':

        component_index,\
        chain_index,\
        molecule_index, molecule_type,\
        entity_index, entity_name = get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                        component_index=True,
                                        chain_index=True,
                                        molecule_index=True, molecule_type=True,
                                        entity_index=True, entity_name=True)

        n_atoms = [ get(item, target=target, indices=index, n_atoms=True) for index in component_index ]
        n_groups = [ get(item, target=target, indices=index, n_groups=True) for index in component_index ]


        return df({'index':component_index,
                   'n atoms':n_atoms, 'n groups':n_groups,
                   'chain index':chain_index,
                   'molecule index':molecule_index, 'molecule type':molecule_type,
                   'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

    elif target=='chain':

        chain_index, chain_id, chain_name,\
        molecule_index, molecule_type,\
        entity_index, entity_name = get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                        chain_index=True, chain_id=True, chain_name=True,
                                        molecule_index=True, molecule_type=True,
                                        entity_index=True, entity_name=True)

        n_atoms = [ get(item, target=target, indices=index, n_atoms=True) for index in chain_index ]
        n_groups = [ get(item, target=target, indices=index, n_groups=True) for index in chain_index ]
        n_components = [ get(item, target=target, indices=index, n_components=True) for index in chain_index ]

        if len(molecule_index.shape)>1:
            n_objects = molecule_index.shape[0]
            aux_obj1_array = _empty([n_objects], dtype='object')
            aux_obj2_array = _empty([n_objects], dtype='object')
            for ii in range(n_objects):
                aux_obj1_array[ii]=molecule_index[ii]
                aux_obj2_array[ii]=molecule_type[ii]
            molecule_index=aux_obj1_array
            molecule_type=aux_obj2_array

        for ii in range(len(molecule_index)):
            if len(molecule_index[ii])==1:
                molecule_index[ii]=molecule_index[ii][0]
                molecule_type[ii]=molecule_type[ii][0]

        return df({'index':chain_index, 'id':chain_id, 'name':chain_name,
                   'n atoms':n_atoms, 'n groups':n_groups, 'n components':n_components,
                   'molecule index':molecule_index, 'molecule type':molecule_type,
                   'entity index':entity_index, 'entity name':entity_name}).style.hide_index()

    elif target=='molecule':

        molecule_index, molecule_name, molecule_type,\
        chain_index,\
        entity_index, entity_name = get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                        molecule_index=True, molecule_name=True, molecule_type=True,
                                        chain_index=True,
                                        entity_index=True, entity_name=True)

        n_atoms = [ get(item, target=target, indices=index, n_atoms=True) for index in molecule_index ]
        n_groups = [ get(item, target=target, indices=index, n_groups=True) for index in molecule_index ]
        n_components = [ get(item, target=target, indices=index, n_components=True) for index in molecule_index ]

        if len(chain_index.shape)>1:
            n_objects = chain_index.shape[0]
            aux_obj_array = _empty([n_objects], dtype='object')
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

        entity_index, entity_name, entity_type = get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                                        entity_index=True, entity_name=True, entity_type=True)

        n_atoms = [ get(item, target=target, indices=index, n_atoms=True) for index in entity_index ]
        n_groups = [ get(item, target=target, indices=index, n_groups=True) for index in entity_index ]
        n_components = [ get(item, target=target, indices=index, n_components=True) for index in entity_index ]
        n_chains = [ get(item, target=target, indices=index, n_chains=True) for index in entity_index ]
        n_molecules = [ get(item, target=target, indices=index, n_molecules=True) for index in entity_index ]


        return df({'index':entity_index, 'name':entity_name, 'type': entity_type,
                   'n atoms':n_atoms, 'n groups':n_groups, 'n components':n_components,
                   'n chains':n_chains, 'n molecules':n_molecules
                   }).style.hide_index()

    elif target=='system':

        form, n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities = get(item, target=target,
                form=True, n_atoms=True, n_groups=True, n_components=True, n_chains=True, n_molecules=True, n_entities=True)

        n_ions, n_waters, n_cosolutes, n_small_molecules, n_peptides, n_proteins, n_dnas, n_rnas = get(item, target=target,
                n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True, n_peptides=True, n_proteins=True,
                n_dnas=True, n_rnas=True)

        n_frames = get(item, target=target, n_frames=True)

        tmp_df = df({'form':form, 'n atoms':n_atoms, 'n groups':n_groups, 'n components':n_components,
            'n chains':n_chains, 'n molecules':n_molecules, 'n entities':n_entities,
            'n waters':n_waters, 'n ions':n_ions, 'n cosolutes':n_cosolutes, 'n small molecules':n_small_molecules,
            'n peptides':n_peptides, 'n proteins':n_proteins, 'n dnas':n_dnas, 'n rnas':n_rnas,
            'n frames':n_frames}, index=[0])

        if n_ions==0: tmp_df.drop(columns=['n ions'], inplace=True)
        if n_waters==0: tmp_df.drop(columns=['n waters'], inplace=True)
        if n_cosolutes==0: tmp_df.drop(columns=['n cosolutes'], inplace=True)
        if n_small_molecules==0: tmp_df.drop(columns=['n small molecules'], inplace=True)
        if n_peptides==0: tmp_df.drop(columns=['n peptides'], inplace=True)
        if n_proteins==0: tmp_df.drop(columns=['n proteins'], inplace=True)
        if n_dnas==0: tmp_df.drop(columns=['n dnas'], inplace=True)
        if n_rnas==0: tmp_df.drop(columns=['n rnas'], inplace=True)

        return tmp_df.style.hide_index()

    else:

        raise NotImplementedError

    pass

def _get_form(item=None):

    from simtk.unit import Quantity

    if type(item) == Quantity:

        from .forms.classes.api_XYZ import this_Quantity_is_XYZ
        if this_Quantity_is_XYZ(item):
            return 'XYZ'
        else:
            raise NotImplementedError("This item's form has not been implemented yet")

    if type(item)==str:

        if ':' in item:
            prefix=item.split(':')[0]
            if prefix+':id' in _dict_ids_is_form.keys():
                item=_dict_ids_is_form[prefix+':id']
            elif prefix+':seq' in _dict_seqs_is_form.keys():
                item=_dict_seqs_is_form[prefix+':seq']
        else:
            item=item.split('.')[-1]

    try:
        return _dict_is_form[type(item)]
    except:
        try:
            return _dict_is_form[item]
        except:
            raise NotImplementedError("This item's form has not been implemented yet")

def get(item, target='atom', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

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

    # selection works as a mask if indices or ids are used

    form_in, _ = _digest_forms(item)
    target = _singular(target)
    attributes = [ key for key in kwargs.keys() if kwargs[key] ]

    # Patch to keep "residue":
    if target=='residue':
        target='group'

    tmp_attributes=[]
    for attribute in attributes:
        if 'residue' in attribute:
            tmp_attributes.append(attribute.replace('residue','group'))
        else:
            tmp_attributes.append(attribute)
    attributes=tmp_attributes

    # doing the work here

    if type(indices)==str:
        if indices in ['all', 'All', 'ALL']:
            indices = 'all'
        else:
            raise ValueError()
    elif type(indices) in [int, _int64, _int]:
        indices = _array([indices], dtype='int64')
    elif hasattr(indices, '__iter__'):
        indices = _array(indices, dtype='int64')

    if indices is None:
        if selection not in ['all', 'All', 'ALL']:
            indices = select(item, target=target, selection=selection, syntaxis=syntaxis)
        else:
            indices = 'all'

    if type(frame_indices)==str:
        if frame_indices in ['all', 'All', 'ALL']:
            frame_indices = 'all'
        else:
            raise ValueError()
    elif type(frame_indices) in [int, _int64, _int]:
        frame_indices = _array([frame_indices], dtype='int64')
    elif hasattr(frame_indices, '__iter__'):
        frame_indices = _array(frame_indices, dtype='int64')


    results = []
    for attribute in attributes:
        result = _dict_get[form_in][target][attribute](item, indices=indices, frame_indices=frame_indices)
        results.append(result)

    if len(results)==1:
        return results[0]
    else:
        return results

def set(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

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


    form_in, _ = _digest_forms(item)
    target = _singular(target)
    attributes = [ key for key in kwargs.keys() ]

    # Patch to keep "residue":
    if target=='residue':
        target='group'

    tmp_attributes=[]
    for attribute in attributes:
        if 'residue' in attribute:
            tmp_attribute = attribute.replace('residue','group')
            tmp_attributes.append(tmp_attribute)
            kwargs [tmp_attribute]= kwargs[attribute]
            del(kwargs[attribute])
        else:
            tmp_attributes.append(attribute)
    attributes=tmp_attributes

    # doing the work here

    if indices is None:
        if target == 'atom':
            indices = select(item, selection=selection, syntaxis=syntaxis)
        elif target == 'group':
            indices = get(item, target='atom', selection=selection, syntaxis=syntaxis, group_index=True)
            indices = list(_unique(indices))
        elif target == 'chain':
            indices = get(item, target='atom', selection=selection, syntaxis=syntaxis, chain_index=True)
            indices = list(_unique(indices))
        elif target == 'system':
            indices = 0

    if frame_indices == 'all':
        n_frames = get(item, target='system', n_frames=True)
        frame_indices = _arange(n_frames)
    elif type(frame_indices)==int:
        frame_indices = [frame_indices]

    for attribute in attributes:
        value = kwargs[attribute]
        _dict_set[form_in][target][attribute](item, indices=indices, frame_indices=frame_indices, value=value)

    pass

def convert(item, to_form='molsysmt.MolSys', selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

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

    form_in, form_out  = _digest_forms(item, to_form)

    if selection is 'all':
        atom_indices='all'
    else:
        atom_indices = select(item, selection=selection, syntaxis=syntaxis)

    out_file = None

    if type(form_out)==str:
        if form_out.split('.')[-1] in _list_files_forms:
            out_file=form_out
            form_out=form_out.split('.')[-1]

    if out_file is not None:
        return _dict_converter[form_in][form_out](item, output_file_path=out_file,
                                                  atom_indices=atom_indices, frame_indices=frame_indices,
                                                  **kwargs)
    else:
        if form_out != form_in:
            return _dict_converter[form_in][form_out](item, atom_indices=atom_indices,
                                                      frame_indices=frame_indices, **kwargs)
        else:
            return extract(item, selection=atom_indices, frame_indices=frame_indices)

def duplicate(item=None):

    form_in, _ = _digest_forms(item)
    return _dict_duplicator[form_in](item)

def write(item=None, filename=None, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    return convert(item, to_form=filename, selection=selection, frame_indices='all', syntaxis=syntaxis)

def view(item=None, viewer='nglview', selection='all', frame_indices='all', syntaxis='MolSysMT'):

    if type(item) in [list,tuple]:
        form_in = _get_form(item[0])
        tmp_item = merge(item)
    else:
        form_in = _get_form(item)
        tmp_item = item

    atom_indices = select(tmp_item, selection=selection, syntaxis=syntaxis)
    frame_indices = _digest_frame_indices(item, frame_indices)

    return _dict_converter[form_in][viewer](tmp_item, atom_indices=atom_indices,
            frame_indices=frame_indices)

