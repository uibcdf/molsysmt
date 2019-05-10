import os
import tempfile

## Items to items:

from .multitool import _dict_converter

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

## Items to viewers

from .multitool import _list_viewers_forms

_dict_viewer_for={}
_dict_to_viewer={}

for _viewer in _list_viewers_forms:
    _dict_to_viewer[_viewer]=_dict_to_from[_viewer]

for in_form in _dict_from_to.keys():
    _dict_viewer_for[in_form]=[]
    for _viewer in _list_viewers_forms:
        if _viewer in _dict_from_to[in_form]:
            _dict_viewer_for[in_form].append(_viewer)



def info_forms(verbose=True):

    tmp_dict={
        'classes':_list_classes_forms,
        'files':_list_files_forms,
        'seqs':_list_seqs_forms,
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


