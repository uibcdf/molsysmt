import os
import tempfile
from .utils.exceptions import *
from .utils.arguments import singular as _singular
from .utils.forms import digest as _digest_forms
from .utils.frame_indices import digest as _digest_frame_indices
from .utils.selection import digest as _digest_selection
from numpy import unique as _unique
from numpy import ndarray as _ndarray
from numpy import sort as _sort
from numpy import arange as _arange

####
#### Molecular Models forms
####

# Classes
from .forms.classes import dict_is_form as _dict_classes_is_form, \
    list_forms as _list_classes_forms, \
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
    dict_converter as _dict_viewers_converter, \
    dict_selector as _dict_viewers_selector, \
    dict_extractor as _dict_viewers_extractor, \
    dict_duplicator as _dict_viewers_duplicator, \
    dict_merger as _dict_viewers_merger, \
    dict_get as _dict_viewers_get, \
    dict_set as _dict_viewers_set

_dict_is_form = {**_dict_classes_is_form, **_dict_files_is_form,\
                 **_dict_ids_is_form, **_dict_seqs_is_form, **_dict_viewers_is_form}
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

####
#### Methods
####

def select(item, selection='all', syntaxis='Pandas'):

    """select(item, selection='all', syntaxis='Pandas')

    Get the atom indices corresponding to a selection criterion.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form (see: :doc:`/Forms`). The object being acted on by the method.

    selection: str, defaul='all'
       Selection criterion given by means of a string following any of the selection syntaxis parsable by MolModMT.

    syntaxis: str, default='Pandas'
       Syntaxis used to write the argument `selection`. The current options supported by MolModMt
       can be found in :doc:`/Atoms_Selection`.

    Returns
    -------

    Numpy array of integers
        List of atom indices in agreement with the selection criterion applied over `item`.

    Examples
    --------

    :doc:`/Atoms_Selection`

    See Also
    --------

    Notes
    -----

    """

    from numpy import array as _array
    from numpy import ndarray as _ndarray
    from numpy import int as _int
    from numpy import int64 as _int64
    from numpy import arange as _arange

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

    atom_indices.sort()
    return atom_indices

def extract(item, selection='all', frame_indices='all', to_form=None, syntaxis='Pandas'):

    """extract(item, selection='all', frame_indices='all', syntaxis='Pandas')

    Extract a subset of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT. (See: XXX)

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolModMT (see: :func:`molmodmt.select`).

    syntaxis: str, default='Pandas'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolModMt can be found in section XXX (see: :func:`molmodmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.select`

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

    """into(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='Pandas')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    to_form: str, default='molmodmt.MolMod'
        Any accepted form by MolModMt for the output object.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolModMT (see: :func:`molmodmt.select`).

    syntaxis: str, default='Pandas'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolModMt can be found in section XXX (see: :func:`molmodmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.get`, :func:`molmodmt.select`
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

def info(item=None, target='system', indices=None, selection='all', syntaxis='Pandas'):

    """into(item, target='system', indices=None, selection='all', syntaxis='Pandas')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT. (See: XXX)

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
       the selection syntaxis parsable by MolModMT.

    syntaxis: str, default='Pandas'
       Selection syntaxis used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolModMt in section 'Selection'.

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.get`, :func:`molmodmt.select`

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

        atom_index, atom_id, atom_name, atom_element, group_index, group_id, group_name, chain_index, chain_id,\
        chain_name, molecule_type = get(item, target=target, indices=indices, selection=selection, syntaxis=syntaxis,
                            index=True, id=True, name=True, element=True,
                            group_index=True, group_id=True, group_name=True,
                            chain_index=True, chain_id=True, chain_name=True,
                            molecule_type=True)

        return df({'index':atom_index, 'id':atom_id, 'name':atom_name, 'element':atom_element,
                   'group index':group_index, 'group id':group_id, 'group name':group_name,
                   'chain index':chain_index, 'chain id':chain_id, 'chain name':chain_name, 'molecule type':molecule_type})

    elif target=='group':

        index, id, name, chain_index, chain_id,\
        molecule_type = get(item, target=target, selection=selection, syntaxis=syntaxis,
                            group_index=True, group_id=True, group_name=True,
                            chain_index=True, chain_id=True, molecule_type=True)


        return df({'name':name, 'index':index, 'id':id, 'chain index':chain_index, 'chain id':chain_id,
                   'molecule type':molecule_type})

    elif target=='component':

        raise NotImplementedError


    elif target=='chain':

        index, id, molecule_type = get(item, target=target, selection=selection, syntaxis=syntaxis,
                                       chain_index=True, chain_id=True, molecule_type=True)

        return df({'index':index, 'id':id, 'molecule type':molecule_type})

    elif target=='molecule':

        raise NotImplementedError

    elif target=='entity':

        raise NotImplementedError

    elif target=='system':

        form, n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities = get(item, target=target,
                form=True, n_atoms=True, n_groups=True, n_components=True, n_chains=True, n_molecules=True, n_entities=True)


        n_ions, n_waters, n_cosolutes, n_small_molecules, n_peptides, n_proteins, n_dnas, n_rnas = get(item, target=target,
                n_ions=True, n_waters=True, n_cosolutes=True, n_small_molecules=True, n_peptides=True, n_proteins=True,
                n_dnas=True, n_rnas=True)

        n_frames = get(item, target=target, n_frames=True)

        tmp_df = df({'form':form, 'atoms':n_atoms, 'groups':n_groups, 'components':n_components,
            'chains':n_chains, 'molecules':n_molecules, 'entities':n_entities,
            'waters':n_waters, 'ions':n_ions, 'cosolutes':n_cosolutes, 'small_molecules':n_small_molecules,
            'peptides':n_peptides, 'proteins':n_proteins, 'dnas':n_dnas, 'rnas':n_rnas,
            'frames':n_frames}, index=[0])

        if n_ions==0: tmp_df.drop(columns=['ions'], inplace=True)
        if n_waters==0: tmp_df.drop(columns=['waters'], inplace=True)
        if n_cosolutes==0: tmp_df.drop(columns=['cosolutes'], inplace=True)
        if n_small_molecules==0: tmp_df.drop(columns=['small_molecules'], inplace=True)
        if n_peptides==0: tmp_df.drop(columns=['peptides'], inplace=True)
        if n_proteins==0: tmp_df.drop(columns=['proteins'], inplace=True)
        if n_dnas==0: tmp_df.drop(columns=['dnas'], inplace=True)
        if n_rnas==0: tmp_df.drop(columns=['rnas'], inplace=True)

        return tmp_df

    else:

        raise NotImplementedError

    pass

def get_form(item=None):

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

def get(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='Pandas', **kwargs):

    """get(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='Pandas')

    Get specific attributes and observables.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT. (See: XXX)

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
       the selection syntaxis parsable by MolModMT.

    syntaxis: str, default='Pandas'
       Selection syntaxis used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolModMt in section 'Selection'.

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        chosen.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.get`, :func:`molmodmt.select`

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

    results = []
    for attribute in attributes:
        result = _dict_get[form_in][target][attribute](item, indices=indices, frame_indices=frame_indices)
        results.append(result)

    if len(results)==1:
        return results[0]
    else:
        return results

def set(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='Pandas', **kwargs):

    """into(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='Pandas')

    Set a new value to an attribute.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT. (See: XXX)

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
       the selection syntaxis parsable by MolModMT (see: :func:`molmodmt.select`).

    frame_indices: int, list, tuple, np.ndarray or 'all', default='all'
        List of indices referring the set of frames this method is going to work with. This set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    syntaxis: str, default='Pandas'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolModMt can be found in section XXX (see: :func:`molmodmt.select`).

    Returns
    -------

    None
        XXX.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.select`

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
        n_frames = get(item, n_frames=True)
        frame_indices = _arange(n_frames)
    elif type(frame_indices)==int:
        frame_indices = [frame_indices]

    for attribute in attributes:
        value = kwargs[attribute]
        _dict_set[form_in][target][attribute](item, indices=indices, frame_indices=frame_indices, value=value)

    pass

def load (item, selection='all', frame_indices='all', to_form='molmodmt.MolMod', syntaxis='Pandas', **kwargs):

    """load(item, selection='all', frame_indices='all', to_form='molmodmt.MolMod', syntaxis='Pandas', **kwargs)

    Loading a molecular model.

    A molecular model coming from a file can be loaded as a new object of any form supported by
    MolModMt (see XXX). This method is just an alias of :func:`molmodmt.convert`. It was included here to make the
    usability more intuitive.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT.

    to_form: str, default='molmodmt.MolMod'
        Any accepted form by MolModMt for the output object.

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolModMT (see: :func:`molmodmt.select`).

    syntaxis: str, default='Pandas'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolModMt can be found in section XXX (see: :func:`molmodmt.select`).

    Returns
    -------

       item: molecular model

       A new object is returned with the form specified by the argument `to_form`.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.convert`, :func:`molmodmt.select`

    Notes
    -----

    """

    return convert(item, selection=selection, frame_indices=frame_indices, to_form=to_form, syntaxis=syntaxis, **kwargs)


def convert(item, to_form='molmodmt.MolMod', selection='all', frame_indices='all', syntaxis='Pandas', **kwargs):

    """convert(item, to_form='molmodmt.MolMod', selection='all', frame_indices='all', syntaxis='Pandas', **kwargs)

    Convert a molecular model into other form.

    A molecular model in a given accepted form can be converted into any other supported form
    by MolModMt. The list of supported forms can be found in the section 'XXX'.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form by MolModMT (see: XXX).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolModMT (see: :func:`molmodmt.select`).

    to_form: str, default='molmodmt.MolMod'
        The output object will take the form specified here. This form supported form by MolModMt
        for the output object.

    syntaxis: str, default='Pandas'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolModMt can be found in section XXX (see: :func:`molmodmt.select`).

    Returns
    -------

       item: molecular model

       A new object is returned with the form specified by the argument `to_form`.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.load`, :func:`molmodmt.select`

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

def write(item=None, filename=None, selection='all', frame_indices='all', syntaxis='Pandas'):

    return convert(item, to_form=filename, selection=selection, frame_indices='all', syntaxis=syntaxis)

def view(item=None, viewer='nglview', selection='all', frame_indices='all', syntaxis='Pandas'):

    if type(item) in [list,tuple]:
        form_in = get_form(item[0])
        tmp_item = merge(item)
    else:
        form_in = get_form(item)
        tmp_item = item

    atom_indices = select(tmp_item, selection=selection, syntaxis=syntaxis)
    frame_indices = _digest_frame_indices(item, frame_indices)

    return _dict_converter[form_in][viewer](tmp_item, atom_indices=atom_indices,
            frame_indices=frame_indices)

