import os
import tempfile
from .utils.exceptions import *
from .utils.arguments import singular as _singular
from .utils.forms import digest_forms as _digest_forms
from numpy import unique as _unique
from numpy import ndarray as _ndarray
from numpy import sort as _sort

####
#### Molecular Models forms
####

# Classes
from .forms.classes import dict_is_form as _dict_classes_is_form, \
    list_forms as _list_classes_forms, \
    dict_n_atoms as _dict_classes_n_atoms, \
    dict_converter as _dict_classes_converter, \
    dict_selector as _dict_classes_selector, \
    dict_extractor as _dict_classes_extractor, \
    dict_trimmer as _dict_classes_trimmer, \
    dict_duplicator as _dict_classes_duplicator, \
    dict_merger as _dict_classes_merger, \
    dict_get as _dict_classes_get, \
    dict_set as _dict_classes_set

# Files
from .forms.files import dict_is_form as _dict_files_is_form, \
    list_forms as _list_files_forms, \
    dict_n_atoms as _dict_files_n_atoms, \
    dict_converter as _dict_files_converter, \
    dict_selector as _dict_files_selector, \
    dict_extractor as _dict_files_extractor, \
    dict_trimmer as _dict_files_trimmer, \
    dict_duplicator as _dict_files_duplicator, \
    dict_merger as _dict_files_merger, \
    dict_get as _dict_files_get, \
    dict_set as _dict_files_set

# IDs
from .forms.ids import dict_is_form as _dict_ids_is_form, \
    list_forms as _list_ids_forms, \
    dict_n_atoms as _dict_ids_n_atoms, \
    dict_converter as _dict_ids_converter, \
    dict_selector as _dict_ids_selector, \
    dict_extractor as _dict_ids_extractor, \
    dict_trimmer as _dict_ids_trimmer, \
    dict_duplicator as _dict_ids_duplicator, \
    dict_merger as _dict_ids_merger, \
    dict_get as _dict_ids_get, \
    dict_set as _dict_ids_set

# Sequences
from .forms.seqs import dict_is_form as _dict_seqs_is_form, \
    list_forms as _list_seqs_forms, \
    dict_n_atoms as _dict_seqs_n_atoms, \
    dict_converter as _dict_seqs_converter, \
    dict_selector as _dict_seqs_selector, \
    dict_extractor as _dict_seqs_extractor, \
    dict_trimmer as _dict_seqs_trimmer, \
    dict_duplicator as _dict_seqs_duplicator, \
    dict_merger as _dict_seqs_merger, \
    dict_get as _dict_seqs_get, \
    dict_set as _dict_seqs_set

# Viewers
from .forms.viewers import dict_is_form as _dict_viewers_is_form, \
    list_forms as _list_viewers_forms, \
    dict_n_atoms as _dict_viewers_n_atoms, \
    dict_converter as _dict_viewers_converter, \
    dict_selector as _dict_viewers_selector, \
    dict_extractor as _dict_viewers_extractor, \
    dict_trimmer as _dict_viewers_trimmer, \
    dict_duplicator as _dict_viewers_duplicator, \
    dict_merger as _dict_viewers_merger, \
    dict_get as _dict_viewers_get, \
    dict_set as _dict_viewers_set

_dict_is_form = {**_dict_classes_is_form, **_dict_files_is_form,\
                 **_dict_ids_is_form, **_dict_seqs_is_form, **_dict_viewers_is_form}
_dict_n_atoms = {**_dict_classes_n_atoms, **_dict_files_n_atoms,\
                   **_dict_ids_n_atoms, **_dict_seqs_n_atoms, **_dict_viewers_n_atoms}
_dict_converter = {**_dict_classes_converter, **_dict_files_converter,\
                   **_dict_ids_converter, **_dict_seqs_converter, **_dict_viewers_converter}
_dict_selector = {**_dict_classes_selector, **_dict_files_selector,\
                   **_dict_ids_selector, **_dict_seqs_selector, **_dict_viewers_selector}
_dict_extractor = {**_dict_classes_extractor, **_dict_files_extractor,\
                   **_dict_ids_extractor, **_dict_seqs_extractor, **_dict_viewers_extractor}
_dict_trimmer = {**_dict_classes_trimmer, **_dict_files_trimmer,\
                   **_dict_ids_trimmer, **_dict_seqs_trimmer, **_dict_viewers_trimmer}
_dict_duplicator = {**_dict_classes_duplicator, **_dict_files_duplicator,\
                   **_dict_ids_duplicator, **_dict_seqs_duplicator, **_dict_viewers_duplicator}
_dict_merger    = {**_dict_classes_merger, **_dict_files_merger,\
                   **_dict_ids_merger, **_dict_seqs_merger, **_dict_viewers_merger}
_dict_get = {**_dict_classes_get, **_dict_files_get,\
                   **_dict_ids_get, **_dict_seqs_get, **_dict_viewers_get}
_dict_set = {**_dict_classes_set, **_dict_files_set,\
                   **_dict_ids_set, **_dict_seqs_set, **_dict_viewers_set}

####
#### Molecular Models attributes
####

# Coordinates
from .attributes.coordinates import list_forms as _list_coordinates_forms, \
    dict_reformatter as _dict_coordinates_reformatter

_dict_reformatter={}
_dict_reformatter['coordinates']=_dict_coordinates_reformatter

_list_attributes = list(_dict_reformatter.keys())

####
#### Methods
####

def select(item, selection='all', syntaxis='mdtraj'):

    from numpy import ndarray as _ndarray
    from numpy import int as _int
    from numpy import int64 as _int64
    from .utils.selection import parse_selection

    form_in, _ = _digest_forms(item)

    if type(selection) in [list, tuple, _ndarray, set]:
        return list(selection)
    elif type(selection) in [int, _int64, _int]:
        return [selection]
    elif selection in ['all', 'All', 'ALL']:
        return list(range(_dict_n_atoms[form_in](item)))
    else:
        selection = parse_selection(selection, syntaxis)
        atom_indices = _dict_selector[form_in][syntaxis](item, selection)
        return list(_sort(atom_indices))

def extract(item, selection='all', form=None, syntaxis='mdtraj'):

    if selection in [None,'all']:
        return item

    form_in, form_out = _digest_forms(item, form)
    atom_indices = select(item=item, selection=selection, syntaxis=syntaxis)
    tmp_item = _dict_extractor[form_in](item, atom_indices)
    tmp_item = convert(tmp_item,form_out)

    return tmp_item

def trim(item, selection=None, form=None, syntaxis='mdtraj'):

    if selection is None:
        return item

    if selection=="all":
        raise BadCallError("Bad selection. All atoms will be removed")

    form_in, form_out = _digest_forms(item, form)
    atom_indices = select(item=item, selection=selection, syntaxis=syntaxis)
    tmp_item = _dict_trimmer[form_in](item, atom_indices)
    tmp_item = convert(tmp_item,form_out)
    return tmp_item

def merge(item1=None, item2=None, form=None):

    #item1 can be a list or tuple

    if type(item1) in [list,tuple]:
        _ , form_out = _digest_forms(item1[0], form)
        tmp_item = convert(item1[0], form_out)
        for in_item in item1[1:]:
            tmp_item2 = convert(in_item, form_out)
            tmp_item = _dict_merger[form](tmp_item, tmp_item2)
        return tmp_item
    else:
        _ , form_out = _digest_forms(item1, form)
        tmp_item1 = convert(item1,form)
        tmp_item2 = convert(item2,form)
        return _dict_merger[form](tmp_item1, tmp_item1)

def info(item=None, element='atom', selection="all", syntaxis="mdtraj"):

    from pandas import DataFrame as df
    form_in, _ = _digest_forms(item)
    element = _singular(element)

    if element=='atom':

        index, id, name, residue_name, residue_index, residue_id, chain_index, chain_id,\
        molecule_type = get(item, element=element, selection=selection, syntaxis=syntaxis,
                            atom_index=True, atom_id=True, atom_name=True, residue_name=True,
                            residue_index=True, residue_id=True, chain_index=True, chain_id=True,
                            molecule_type=True)

        return df({'name':name, 'index':index, 'id':id, 'residue_name':residue_name,
                   'residue index':residue_index, 'residue id':residue_id,
                   'chain index':chain_index, 'chain id':chain_id, 'molecule type':molecule_type})

    elif element=='residue':

        index, id, name, chain_index, chain_id,\
        molecule_type = get(item, element=element, selection=selection, syntaxis=syntaxis,
                            residue_index=True, residue_id=True, residue_name=True,
                            chain_index=True, chain_id=True, molecule_type=True)


        return df({'name':name, 'index':index, 'id':id, 'chain index':chain_index, 'chain id':chain_id,
                   'molecule type':molecule_type})

    elif element=='chain':

        index, id, molecule_type = get(item, element=element, selection=selection, syntaxis=syntaxis,
                                       chain_index=True, chain_id=True, molecule_type=True)

        return df({'index':index, 'id':id, 'molecule type':molecule_type})

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

def get(item, element='atom', indices=None, ids=None, selection='all', syntaxis='mdtraj', **kwargs):

    # selection works as a mask if indices or ids are used

    form_in, _ = _digest_forms(item)
    element = _singular(element)
    singular_kwargs = { _singular(key): kwargs[key] for key in kwargs.keys() }

    if element=='atom':
        if (indices is None) and (ids is None):
            indices=select(item, selection=selection, syntaxis=syntaxis)

    elif element=='residue':
        if (indices is None) and (ids is None):
            indices = get(item, element='atom', selection=selection, syntaxis=syntaxis,
                          residue_index=True)
            indices = list(_unique(indices))

    elif element=='chain':
        if (indices is None) and (ids is None):
            indices = get(item, element='atom', selection=selection, syntaxis=syntaxis,
                          chain_index=True)
            indices = list(_unique(indices))

    elif element=='system':
        indices = get(item, element='atom', selection='all', syntaxis=syntaxis, atom_index=True)

    else:
        raise NotImplementedError

    return _dict_get[form_in](item, element=element, indices=indices, ids=ids, **singular_kwargs)

def set(item=None, element='atom', indices=None, ids=None,  selection='all', syntaxis='mdtraj', **kwargs):

    form_in, _ = _digest_forms(item)
    element = _singular(element)
    singular_kwargs = { _singular(key): kwargs[key] for key in kwargs.keys() }

    if element=='atom':
        if (indices is None) and (ids is None):
            indices=select(item, selection=selection, syntaxis=syntaxis)

    if element=='residue':
        if (indices is None) and (ids is None):
            indices = get(item, element='atom', selection=selection, syntaxis=syntaxis,
                          residue_index=True)

    return _dict_set[form_in](item, element=element, indices=indices, ids=ids, **singular_kwargs)

def load (item=None, form='molmodmt.MolMod', selection='all', syntaxis='mdtraj', **kwargs):

    return convert(item, form, selection=selection, syntaxis=syntaxis, **kwargs)


def convert(item=None, form='molmodmt.MolMod', selection='all', syntaxis='mdtraj', **kwargs):

    form_in, form_out  = _digest_forms(item, form)
    out_file = None

    if type(form_out)==str:
        if form_out.split('.')[-1] in _list_files_forms:
            form_out=form.split('.')[-1]
            out_file=form

    if out_file is not None:
        return _dict_converter[form_in][form_out](item, filename=out_file,
                                                  selection=selection, syntaxis=syntaxis, **kwargs)
    else:
        if form_in!=form_out:
            return _dict_converter[form_in][form_out](item, selection=selection, syntaxis=syntaxis, **kwargs)
        else:
            return item

def duplicate(item=None):

    form_in, _ = _digest_forms(item)

    return _dict_duplicator[form_in](item)

def write(item=None, filename=None, selection='all', syntaxis='mdtraj'):

    return convert(item,filename, selection=selection, syntaxis=syntaxis)

def view(item=None, viewer='nglview', selection='all', syntaxis='mdtraj'):

    if type(item) in [list,tuple]:
        form_in = get_form(item[0])
        tmp_item = merge(item)
    else:
        form_in = get_form(item)
        tmp_item = item

    if selection is not None:
        tmp_item = extract(tmp_item, selection=selection, syntaxis=syntaxis)

    return _dict_converter[form_in][viewer](tmp_item)

def reformat(attribute=None, value=None, is_format=None, to_format=None):

    if (attribute is not None) and attribute in _list_attributes:
        if is_format is not None:
            if to_format is not None:

                return _dict_reformatter[attribute][is_format][to_format](value)

            else:
                raise BadCallError(BadCallMessage)
        else:
            raise BadCallError(BadCallMessage)
    else:
        raise BadCallError(BadCallMessage)

