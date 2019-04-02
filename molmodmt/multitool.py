import os
import tempfile

## Engines
from .formats.engines import dict_is_form as _dict_engines_is_form, \
    list_forms as _list_engines_forms, \
    dict_converter as _dict_engines_converter, \
    dict_selector as _dict_engines_selector, \
    dict_extractor as _dict_engines_extractor, \
    dict_merger as _dict_engines_merger, \
    dict_get as _dict_engines_get

## Classes
from .formats.classes import dict_is_form as _dict_classes_is_form, \
    list_forms as _list_classes_forms, \
    dict_converter as _dict_classes_converter, \
    dict_selector as _dict_classes_selector, \
    dict_extractor as _dict_classes_extractor, \
    dict_merger as _dict_classes_merger, \
    dict_get as _dict_classes_get

## Files
from .formats.files import dict_is_form as _dict_files_is_form, \
    list_forms as _list_files_forms, \
    dict_converter as _dict_files_converter, \
    dict_selector as _dict_files_selector, \
    dict_extractor as _dict_files_extractor, \
    dict_merger as _dict_files_merger, \
    dict_get as _dict_files_get

## IDs
from .formats.ids import dict_is_form as _dict_ids_is_form, \
    list_forms as _list_ids_forms, \
    dict_converter as _dict_ids_converter, \
    dict_selector as _dict_ids_selector, \
    dict_extractor as _dict_ids_extractor, \
    dict_merger as _dict_ids_merger, \
    dict_get as _dict_ids_get

## Sequences
from .formats.seqs import dict_is_form as _dict_seqs_is_form, \
    list_forms as _list_seqs_forms, \
    dict_converter as _dict_seqs_converter, \
    dict_selector as _dict_seqs_selector, \
    dict_extractor as _dict_seqs_extractor, \
    dict_merger as _dict_seqs_merger, \
    dict_get as _dict_seqs_get

## Viewers
from .formats.viewers import dict_is_form as _dict_viewers_is_form, \
    list_forms as _list_viewers_forms, \
    dict_converter as _dict_viewers_converter, \
    dict_selector as _dict_viewers_selector, \
    dict_extractor as _dict_viewers_extractor, \
    dict_merger as _dict_viewers_merger, \
    dict_get as _dict_viewers_get

_dict_is_form = {**_dict_engines_is_form, **_dict_classes_is_form, **_dict_files_is_form,\
                 **_dict_ids_is_form, **_dict_seqs_is_form, **_dict_viewers_is_form}
_dict_converter = {**_dict_engines_converter, **_dict_classes_converter, **_dict_files_converter,\
                   **_dict_ids_converter, **_dict_seqs_converter, **_dict_viewers_converter}
_dict_selector = {**_dict_engines_selector, **_dict_classes_selector, **_dict_files_selector,\
                   **_dict_ids_selector, **_dict_seqs_selector, **_dict_viewers_selector}
_dict_extractor = {**_dict_engines_extractor, **_dict_classes_extractor, **_dict_files_extractor,\
                   **_dict_ids_extractor, **_dict_seqs_extractor, **_dict_viewers_extractor}
_dict_merger    = {**_dict_engines_merger, **_dict_classes_merger, **_dict_files_merger,\
                   **_dict_ids_merger, **_dict_seqs_merger, **_dict_viewers_merger}
_dict_get = {**_dict_engines_get, **_dict_classes_get, **_dict_files_get,\
                   **_dict_ids_get, **_dict_seqs_get, **_dict_viewers_get}
_dict_from_to = {}
_dict_to_from = {}

for in_form in _dict_converter.keys():
    _dict_from_to[in_form]=_dict_converter[in_form].keys()

for in_form, out_forms in _dict_from_to.items():
    for out_form in out_forms:
        try:
            _dict_to_from[out_form].append(in_form)
        except:
            _dict_to_from[out_form]=[]
            _dict_to_from[out_form].append(in_form)

for in_form in _dict_from_to.keys():
    _dict_from_to[in_form]=sorted(_dict_from_to[in_form])

for out_form in _dict_to_from.keys():
    _dict_to_from[out_form]=sorted(_dict_to_from[out_form])

_dict_viewer_for={}
_dict_to_viewer={}

for _viewer in _list_viewers_forms:
    _dict_to_viewer[_viewer]=_dict_to_from[_viewer]

for in_form in _dict_from_to.keys():
    _dict_viewer_for[in_form]=[]
    for _viewer in _list_viewers_forms:
        if _viewer in _dict_from_to[in_form]:
            _dict_viewer_for[in_form].append(_viewer)

def fetch(form_id=None, form=None):

    return convert(form_id, form)

def select(item=None, selection=None, syntaxis='mdtraj'):

    from numpy import ndarray as _ndarray
    from numpy import int as _int
    from numpy import int64 as _int64

    in_form=get_form(item)

    if type(selection) in [list,tuple,_ndarray]:
        return selection
    elif type(selection) in [int, _int64, _int]:
        return [selection]
    else:
        return _dict_selector[in_form][syntaxis](item, selection)

def extract(item=None, selection=None, form=None, syntaxis='mdtraj'):

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
            tmp_item=_dict_merger[form](tmp_item,convert(item2,form),in_place=in_place)
            return tmp_item

def info(item=None):

    in_form = get_form(item)
    n_atoms, n_frames = get(item,n_atoms=True,n_frames=True)
    print(in_form, "with", num_frames, "frames and", num_atoms, "atoms.")
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

def get(item=None, selection=None, **kwargs):

    in_form = get_form(item)
    if selection is not None:
        atoms_list=select(item,selection=selection)
    else:
        atoms_list=None

    return _dict_get[in_form](item, atoms_list=atoms_list,**kwargs)

def load (item=None, form='molmod', selection=None, pdbfix=False, pH=7.0, verbose=False, **kwargs):

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

        tmp_item = convert(item, form, **kwargs)

    if selection is not None:
        tmp_item = extract(tmp_item,selection)

    return tmp_item

def convert(item=None, form='molmodmt.MolMod', **kwargs):

    #**kwargs: topology=None

    in_form  = get_form(item)
    out_form = form
    out_file = None

    if type(out_form)==str:
        if out_form.split('.')[-1] in _list_files_forms:
            out_form=form.split('.')[-1]
            out_file=form

    if out_file is not None:
        return _dict_converter[in_form][out_form](item, out_file, **kwargs)
    else:
        if in_form!=out_form:
            return _dict_converter[in_form][out_form](item, **kwargs)
        else:
            return item

def write(item=None,filename=None):

    return convert(item,filename)

def view(item=None,selection=None,viewer='nglview'):

    if type(item) in [list,tuple]:
        in_form = get_form(item[0])
    else:
        in_form = get_form(item)

    if selection is not None:
        tmp_item = extract(item,selection)
    else:
        tmp_item = item

    return _dict_converter[in_form][viewer](tmp_item)

def info_forms(engines=True,classes=True,files=True,verbose=True):

    tmp_dict={
        'engines':_list_engines_forms,
        'classes':_list_classes_forms,
        'files':_list_files_forms,
        'ids': _list_ids_forms
        }

    return tmp_dict

def info_load(from_form=None,to_form=None,verbose=True):

    return info_convert(from_form,to_form,verbose)

def info_convert(from_form=None,to_form=None,verbose=True):

    tmp_output=None

    if from_form is not None:
        if to_form is not None:
            if to_form in _dict_from_to[from_form]:
                tmp_output= True
            else:
                tmp_output= False
        else:
            tmp_output=_dict_from_to[from_form]
    elif to_form is not None:
        tmp_output=_dict_to_from[to_form]
    else:
        if verbose:
            print('From... to...')
            for key in _dict_from_to.keys():
                print(key,': ',_dict_from_to[key])
            print('\nTo... from...')
            for key in _dict_to_from.keys():
                print(key,': ',_dict_to_from[key])
            pass

    if (tmp_output is not None) and verbose:
        print(tmp_output)
    else:
        pass

def info_select():
    pass

def info_viewers(for_form=None,to_viewer=None):

    if for_form is not None:
        if to_viewer is not None:
            pass
        else:
            return _dict_viewer_for[for_form]
    else:
        if to_viewer is not None:
            return _dict_to_viewer[to_viewer]
        else:
            pass


