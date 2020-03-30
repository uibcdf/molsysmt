from .utils.exceptions import *
from .multitool import _list_classes_forms, _list_files_forms, _list_ids_forms, _list_seqs_forms, _list_viewers_forms, _list_types
from .multitool import _dict_infotxt, _dict_type, _dict_converter

list_classes_forms = sorted(_list_classes_forms)
list_files_forms = sorted(_list_files_forms)
list_ids_forms = sorted(_list_ids_forms)
list_seqs_forms = sorted(_list_seqs_forms)
list_viewers_forms = sorted(_list_viewers_forms)
list_forms = list_classes_forms + list_files_forms + list_ids_forms + list_seqs_forms + list_viewers_forms
list_types = _list_types

convert_from = {}
convert_to = {}

for in_form in _dict_converter.keys():
    convert_from[in_form]=_dict_converter[in_form].keys()

for in_form, out_forms in convert_from.items():
    for out_form in out_forms:
        try:
            convert_to[out_form].append(in_form)
        except:
            convert_to[out_form]=[]
            convert_to[out_form].append(in_form)

for in_form in convert_from.keys():
    convert_from[in_form]=sorted(convert_from[in_form])

for out_form in convert_to.keys():
    convert_to[out_form]=sorted(convert_to[out_form])

## Types

def info_forms(form_type=None,verbose=True):

    tmp_output = []

    if form_type in [None,'all']:
        tmp_output=list_forms
    elif form_type is 'class':
        tmp_output=list_classes_forms
    elif form_type is 'file':
        tmp_output=list_files_forms
    elif form_type is 'id':
        tmp_output=list_ids_forms
    elif form_type is 'seq':
        tmp_output=list_seqs_forms
    elif form_type is 'viewer':
        tmp_output=list_viewers_forms
    else:
        raise BadCallError(BadCallMessage)

    if verbose:

        from pandas import DataFrame

        df=DataFrame([[form, _dict_type[form], _dict_infotxt[form]] for form in tmp_output], columns=['Form', 'Type', 'Info'])
        def make_clickable(val):
            return '<a target="_blank" href="{}">{}</a>'.format(val[1], val[0])
        return df.style.hide_index().format({'Info':make_clickable}).set_properties(**{'text-align':'left','colheader_justify':'left'}).\
            set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])

    else:

        return tmp_output

def info_load(from_form=None, to_form=None, from_form_type=None, to_form_type=None, verbose=True):

    return info_convert(from_form, to_form, from_form_type, to_form_type, verbose)

def info_convert(from_form=None, to_form=None, from_form_type=None, to_form_type=None, verbose=True):

    tmp_output=None

    if from_form is not None:
        if to_form is not None:
            if to_form in _dict_from_to[from_form]:
                tmp_output= True
            elif to_form_type in dict:
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


