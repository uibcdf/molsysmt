from importlib import import_module
import os

types = ['class', 'file', 'string']
forms = []

dict_type = {}
dict_is_form = {}
dict_info = {}
dict_add = {}
dict_merge = {}
dict_append_frames = {}
dict_concatenate_frames = {}
dict_convert = {}
dict_get = {}
dict_set = {}
dict_has = {}
dict_extract = {}

file_extensions_recognized = []
string_names_recognized = []

current_dir = os.path.dirname(os.path.abspath(__file__))

list_apis = [filename.split('.')[0] for filename in os.listdir(current_dir) if filename.startswith('api_')]

for api_name in list_apis:

    mod = import_module('molsysmt.api_forms.'+api_name)

    form_name = mod.form_name
    forms.append(form_name)

    if form_name.startswith('string:'):
        form_type = 'string'
    elif form_name.startswith('file:'):
        form_type = 'file'
    else:
        form_type = 'class'

    dict_type[form_name]=form_type
    dict_is_form.update(mod.is_form)
    dict_info[form_name]=mod.info
    dict_add[form_name]=mod.add
    dict_merge[form_name]=mod.merge
    dict_append_frames[form_name]=mod.append_frames
    dict_concatenate_frames[form_name]=mod.concatenate_frames
    dict_extract[form_name]=mod.extract

    dict_has[form_name]= mod.has

    dict_convert[form_name]= {}
    dict_get[form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                          'entity':{}, 'system':{}, 'bond':{}}
    dict_set[form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                          'entity':{}, 'system':{}, 'bond':{}}

    for method in mod.__dict__.keys():
        if method.startswith('to_'):
            if converts_to_be_loaded[api_name][method]:
                if method.startswith('to_string_'):
                    out_form_name=method.replace('to_string_','string:')
                elif method.startswith('to_file_'):
                    out_form_name=method.replace('to_file_','file:')
                else:
                    out_form_name=method.replace('to_','').replace('_','.',1)
                dict_convert[form_name][out_form_name]= getattr(mod, method)
        if method.startswith('get_'):
            option, target = method[4:].split('_from_')
            dict_get[form_name][target][option]=getattr(mod, method)
        if method.startswith('set_'):
            option, target = method[4:].split('_to_')
            dict_set[form_name][target][option]=getattr(mod, method)

    del(mod, form_name, form_type)

del(list_apis, import_module)

for aux_form_name in list(dict_is_form.keys()):
    if type(aux_form_name) is str:
        if aux_form_name.startswith('file:'):
            file_extensions_recognized.append(aux_form_name.split(':')[-1].lower())
        elif aux_form_name.startswith('string:'):
            string_names_recognized.append(aux_form_name.split(':')[-1])

