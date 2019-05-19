import os
import tempfile
from .utils.exceptions import *
from .utils.arguments import singular as _singular

#### Molecular Models forms

## Classes
from .forms.classes import dict_is_form as _dict_classes_is_form, \
    list_forms as _list_classes_forms, \
    dict_converter as _dict_classes_converter, \
    dict_selector as _dict_classes_selector, \
    dict_extractor as _dict_classes_extractor, \
    dict_trimmer as _dict_classes_trimmer, \
    dict_adder as _dict_classes_adder,\
    dict_duplicator as _dict_classes_duplicator, \
    dict_merger as _dict_classes_merger, \
    dict_get as _dict_classes_get, \
    dict_set as _dict_classes_set

## Files
from .forms.files import dict_is_form as _dict_files_is_form, \
    list_forms as _list_files_forms, \
    dict_converter as _dict_files_converter, \
    dict_selector as _dict_files_selector, \
    dict_extractor as _dict_files_extractor, \
    dict_trimmer as _dict_files_trimmer, \
    dict_adder as _dict_files_adder, \
    dict_duplicator as _dict_files_duplicator, \
    dict_merger as _dict_files_merger, \
    dict_get as _dict_files_get, \
    dict_set as _dict_files_set

## IDs
from .forms.ids import dict_is_form as _dict_ids_is_form, \
    list_forms as _list_ids_forms, \
    dict_converter as _dict_ids_converter, \
    dict_selector as _dict_ids_selector, \
    dict_extractor as _dict_ids_extractor, \
    dict_trimmer as _dict_ids_trimmer, \
    dict_adder as _dict_ids_adder, \
    dict_duplicator as _dict_ids_duplicator, \
    dict_merger as _dict_ids_merger, \
    dict_get as _dict_ids_get, \
    dict_set as _dict_ids_set

## Sequences
from .forms.seqs import dict_is_form as _dict_seqs_is_form, \
    list_forms as _list_seqs_forms, \
    dict_converter as _dict_seqs_converter, \
    dict_selector as _dict_seqs_selector, \
    dict_extractor as _dict_seqs_extractor, \
    dict_trimmer as _dict_seqs_trimmer, \
    dict_adder as _dict_seqs_adder, \
    dict_duplicator as _dict_seqs_duplicator, \
    dict_merger as _dict_seqs_merger, \
    dict_get as _dict_seqs_get, \
    dict_set as _dict_seqs_set

## Viewers
from .forms.viewers import dict_is_form as _dict_viewers_is_form, \
    list_forms as _list_viewers_forms, \
    dict_converter as _dict_viewers_converter, \
    dict_selector as _dict_viewers_selector, \
    dict_extractor as _dict_viewers_extractor, \
    dict_trimmer as _dict_viewers_trimmer, \
    dict_adder as _dict_viewers_adder, \
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
_dict_trimmer = {**_dict_classes_trimmer, **_dict_files_trimmer,\
                   **_dict_ids_trimmer, **_dict_seqs_trimmer, **_dict_viewers_trimmer}
_dict_adder = {**_dict_classes_adder, **_dict_files_adder,\
                   **_dict_ids_adder, **_dict_seqs_adder, **_dict_viewers_adder}
_dict_duplicator = {**_dict_classes_duplicator, **_dict_files_duplicator,\
                   **_dict_ids_duplicator, **_dict_seqs_duplicator, **_dict_viewers_duplicator}
_dict_merger    = {**_dict_classes_merger, **_dict_files_merger,\
                   **_dict_ids_merger, **_dict_seqs_merger, **_dict_viewers_merger}
_dict_get = {**_dict_classes_get, **_dict_files_get,\
                   **_dict_ids_get, **_dict_seqs_get, **_dict_viewers_get}
_dict_set = {**_dict_classes_set, **_dict_files_set,\
                   **_dict_ids_set, **_dict_seqs_set, **_dict_viewers_set}

#### Attributes

## Coordinates
from .attributes.coordinates import list_forms as _list_coordinates_forms, \
    dict_reformatter as _dict_coordinates_reformatter

_dict_reformatter={}
_dict_reformatter['coordinates']=_dict_coordinates_reformatter

_list_attributes = list(_dict_reformatter.keys())

def fetch(form_id=None, form=None):

    return convert(form_id, form)

def select(item=None, selection='all', syntaxis='mdtraj'):

    from numpy import ndarray as _ndarray
    from numpy import int as _int
    from numpy import int64 as _int64
    from .utils.selection import parse_selection

    in_form=get_form(item)

    if type(selection) in [list,tuple,_ndarray]:
        return selection
    elif type(selection) in [int, _int64, _int]:
        return [selection]
    else:
        selection = parse_selection(selection, syntaxis)
        return _dict_selector[in_form][syntaxis](item, selection)

def extract(item=None, selection='all', form=None, syntaxis='mdtraj'):

    if selection is None:
        return item

    from numpy import ndarray as _ndarray
    from numpy import sort as _sort

    in_form=get_form(item)
    if form is None:
        form=in_form

    if type(selection) == int:
        list_atoms=[selection]
    elif type(selection) in [list,tuple]:
        list_atoms=selection
    elif type(selection) == _ndarray:
        list_atoms=selection
    else:
        list_atoms = select(item=item, selection=selection, syntaxis=syntaxis) # list_atoms 0-based
    list_atoms = _sort(list_atoms)
    extraction = _dict_extractor[in_form](item, list_atoms)
    del(_ndarray,_sort,list_atoms)
    return convert(extraction,form)

def merge(item1=None, item2=None, in_place=False, form=None):

    #item1 can be a list or tuple

    if type(item1) in [list,tuple]:
        if form is None:
            form=get_form(item1[0])
        tmp_item = convert(item1[0],form)
        for in_item in item1[1:]:
            tmp_item = _dict_merger[form](tmp_item,convert(in_item,form))
        return tmp_item
    else:
        if form is None:
            form=get_form(item1)
        tmp_item = convert(item1,form)
        if in_place:
            _dict_merger[form](tmp_item,convert(in_item,form),in_place=in_place)
            pass
        else:
            tmp_item=_dict_merger[form](tmp_item,convert(item2,form))
            return tmp_item

def info(item=None, element='atom', selection="all", syntaxis="mdtraj", format='pandas'):

    in_form = get_form(item)

    element = _singular(element)

    if element=='atom':

        wrap_arguments = get(item, element=element, selection=selection, syntaxis=syntaxis,
                             atom_index=True, atom_id=True, atom_name=True, residue_index=True,
                             chain_index=True, molecule_type=True)

        if format=='text':
            for index, id, name, residue_index, chain_index in zip(*wrap_arguments):
                print("{} with index {} and id {} in residue with ".format(name, index, id)+
                      "index {}, chain with index {} and molecule ".format(residue_index, chain_index)+
                      "type {}".format(molecule_type))

        elif format=='pandas':
            from pandas import DataFrame as df
            index, id, name, chain_index, molecule_type = wrap_arguments
            return df({'Name':name, 'index':index, 'id':id, 'chain index':chain_index, 'molecule type':molecule_type})

    elif element=='residue':

        wrap_arguments= get(item, element=element, selection=selection, syntaxis=syntaxis,
                            residue_index=True, residue_id=True, residue_name=True,
                            chain_index=True, molecule_type=True)

        if format=='text':
            for index, id, name, chain_index, molecule_type in zip(*wrap_argments):
                print("{} with index {} and id {} in chain with index {} and molecule type {}".format(name, index, id, chain_index, molecule_type))

        elif format=='pandas':
            from pandas import DataFrame as df
            index, id, name, chain_index, molecule_type = wrap_arguments
            return df({'Name':name, 'index':index, 'id':id, 'chain index':chain_index, 'molecule type':molecule_type})

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

    in_form = get_form(item)

    element = _singular(element)
    singular_kwargs = { _singular(key): kwargs[key] for key in kwargs.keys() }

    if element=='atom':
        if (indices is None) and (ids is None):
            indices=select(item, selection=selection, syntaxis=syntaxis)

    if element=='residue':
        if (indices is None) and (ids is None):
            indices = get(item, element='atom', selection=selection, syntaxis=syntaxis,
                          residue_index=True)

    return _dict_get[in_form](item, element=element, indices=indices, ids=ids, **singular_kwargs)

def set(item=None, selection='all', **kwargs):

    in_form = get_form(item)
    singular_kwargs = { _singular(key): kwargs[key] for key in kwargs.keys() }

    atom_indices=select(item,selection=selection)

    return _dict_set[in_form](item, atom_indices=atom_indices, **singular_kwargs)

def load (item=None, form='molmodmt.MolMod', selection='all', pdbfix=False, pH=7.0, verbose=False, **kwargs):

    #**kwargs: topology=None

    if pdbfix == True:

        in_form = get_form(item)

        if in_form not in ['pdb:id','pdb']:
            raise NotImplementedError("pdbfix only works with 'pdb:id' or 'pdb' forms")

        tmp_pdbfixer_form = convert(item,'pdbfixer.PDBFixer')

        tmp_pdbfixer_form.findMissingResidues()
        tmp_pdbfixer_form.findNonstandardResidues()
        if verbose :
            print(tmp_pdbfixer_form.missingResidues)
            print(tmp_pdbfixer_form.nonstandardResidues)

        tmp_pdbfixer_form.replaceNonstandardResidues()
        tmp_pdbfixer_form.findMissingAtoms()

        if verbose :
            print(tmp_pdbfixer_form.missingAtoms)

        tmp_pdbfixer_form.addMissingAtoms()
        tmp_pdbfixer_form.addMissingHydrogens(pH)

        tmp_item = convert(tmp_pdbfixer_form,form)

    else:

        tmp_item = convert(item, form, selection=selection, **kwargs)

    #if selection is not None:
    #    tmp_item = extract(tmp_item,selection)

    return tmp_item

def convert(item=None, form='molmodmt.MolMod', selection='all', syntaxis='mdtraj', **kwargs):

    #**kwargs: topology=None

    in_form  = get_form(item)
    out_form = form
    out_file = None

    if type(out_form)==str:
        if out_form.split('.')[-1] in _list_files_forms:
            out_form=form.split('.')[-1]
            out_file=form

    if out_file is not None:
        return _dict_converter[in_form][out_form](item, filename=out_file, selection=selection,
                                                  syntaxis=syntaxis, **kwargs)
    else:
        if in_form!=out_form:
            return _dict_converter[in_form][out_form](item, selection=selection, syntaxis=syntaxis, **kwargs)
        else:
            return item

def duplicate(item=None):

    in_form = get_form(item)

    return _dict_duplicator[in_form](item)

def write(item=None,filename=None, selection='all', syntaxis='mdtraj'):

    return convert(item,filename, selection=selection, syntaxis=syntaxis)

def view(item=None, viewer='nglview', selection='all', syntaxis='mdtraj'):

    if type(item) in [list,tuple]:
        in_form = get_form(item[0])
        tmp_item = merge(item)
    else:
        in_form = get_form(item)
        tmp_item = item

    if selection is not None:
        tmp_item = extract(tmp_item, selection=selection, syntaxis=syntaxis)

    return _dict_converter[in_form][viewer](tmp_item)

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

