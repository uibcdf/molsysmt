## Engines
from .formats.engines import dict_is_form as _dict_engines_is_form, \
        list_forms as _list_engines_forms, \
        dict_converter as _dict_engines_converter, \
        dict_get_shape as _dict_engines_get_shape

## Classes
from .formats.classes import dict_is_form as _dict_classes_is_form, \
        list_forms as _list_classes_forms, \
        dict_converter as _dict_classes_converter, \
        dict_get_shape as _dict_classes_get_shape

## Files
from .formats.files import dict_is_form as _dict_files_is_form, \
        list_forms as _list_files_forms, \
        dict_converter as _dict_files_converter, \
        dict_get_shape as _dict_files_get_shape

## Viewers
from .formats.viewers import dict_is_form as _dict_viewers_is_form, \
        list_forms as _list_viewers_forms, \
        dict_converter as _dict_viewers_converter, \
        dict_get_shape as _dict_viewers_get_shape

_dict_is_form = {**_dict_engines_is_form, **_dict_classes_is_form, **_dict_files_is_form,\
                 **_dict_viewers_is_form}
_dict_converter = {**_dict_engines_converter, **_dict_classes_converter, **_dict_files_converter,\
                   **_dict_viewers_converter}
_dict_get_shape = {**_dict_engines_get_shape, **_dict_classes_get_shape, **_dict_files_get_shape,\
                   **_dict_viewers_get_shape}

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

def info(item=None, with_form=False):

    if with_form:
        in_form = get_form(item)
    else:
        in_form = "Trajectory"

    num_frames, num_atoms = get_shape(item)

    print(in_form, "with", num_frames, "frames and", num_atoms, "atoms.")
    pass

def get_form(item=None):

    if type(item)==str:
        if ':' in item:
            item=item.split(':')[0]+":id"
        else:
            item=item.split('.')[-1]

    try:
        return _dict_is_form[type(item)]
    except:
        try:
            return _dict_is_form[item]
        except:
            raise NotImplementedError("This item's form has not been implemented yet")

def get_shape(item=None):

    in_form = get_form(item)

    return _dict_get_shape[in_form](item)

def load (item=None,form='native.Native'):

    return convert(item,form)

def select (item=None, selection=None, syntaxis='native'):

    from molsysmt.multitool import select as _select
    tmp_output_selection = _select(item, selection, syntaxis)
    del(_select)
    return tmp_output_selection

def convert(item=None,form=None):

    in_form  = get_form(item)
    out_form = form
    out_file = None

    if type(out_form)==str:
        if out_form.split('.')[-1] in _list_files_forms:
            out_form=form.split('.')[-1]
            out_file=form

    if out_file is not None:
        return _dict_converter[in_form][out_form](item,out_file)
    else:
        if (in_form.startswith(out_form)):
            return item
        else:
            return _dict_converter[in_form][out_form](item)

def extract(item=None):

    pass

def view(item=None,viewer='nglview'):

    in_form = get_form(item)
    return _dict_converter[in_form][viewer](item)

def info_forms(engines=True,classes=True,files=True,verbose=True):

    tmp_dict={
        'engines':_list_engines_forms,
        'classes':_list_classes_forms,
        'files':_list_files_forms
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
