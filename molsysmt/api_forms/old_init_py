from importlib import import_module
import os

dict_is_form = {}
dict_type = {}
dict_info = {}
dict_attributes = {}
dict_extract = {}
dict_add = {}
dict_append_structures = {}
dict_structures_iterator = {}
dict_topology_iterator = {}
dict_get = {}
dict_set = {}
dict_convert = {}
forms = []
file_forms = []
string_forms = []

current_dir = os.path.dirname(os.path.abspath(__file__))
apis = [filename.split('.')[0] for filename in os.listdir(current_dir) if filename.startswith('api_')]

for api_name in apis:

    name = api_name.replace('api_','')
    mod_api = import_module('molsysmt.api_forms.' + api_name)
    mod = import_module('molsysmt.form.' + name)

    forms.append(mod.form_name)

    if mod.form_type=='file':
        file_forms.append(mod.form_name)
    elif mod.form_type=='string':
        string_forms.append(mod.form_name)

    dict_type[mod.form_name] = mod.form_type
    dict_info[mod.form_name] = mod.form_info
    dict_attributes[mod.form_name] = mod.attributes     

    dict_add[mod.form_name] = mod.add
    dict_append_structures[mod.form_name] = mod.append_structures
    dict_structures_iterator[mod.form_name] = mod.StructuresIterator
    dict_topology_iterator[mod.form_name] = mod.TopologyIterator
    dict_extract[mod.form_name] = mod.extract
    dict_is_form[mod.form_name] = getattr(mod, 'is_'+name)


    dict_get[mod.form_name] = {
        'atom': {},
        'group': {},
        'component': {},
        'molecule': {},
        'chain': {},
        'entity': {},
        'system': {},
        'bond': {},
    }

    dict_set[mod.form_name] = {
        'atom': {},
        'group': {},
        'component': {},
        'molecule': {},
        'chain': {},
        'entity': {},
        'system': {},
        'bond': {},
    }


    dict_convert[mod.form_name] = {}

    for method in mod_api.__dict__.keys():
        if method.startswith('to_'):
            if method.startswith('to_string_'):
                out_form_name=method.replace('to_string_','string:')
            elif method.startswith('to_file_'):
                out_form_name=method.replace('to_file_','file:')
            else:
                out_form_name=method.replace('to_','').replace('_','.')
            dict_convert[mod.form_name][out_form_name]= getattr(mod_api, method)

    for method in mod.__dict__.keys():
        if method.startswith('get_') and '_from_' in method:
            option, element = method[4:].split('_from_')
            dict_get[mod.form_name][element][option]=getattr(mod, method)
        elif method.startswith('set_') and '_to_' in method:
            option, element = method[4:].split('_to_')
            dict_set[mod.form_name][element][option]=getattr(mod, method)

del(mod, mod_api, method, out_form_name, api_name, name)
del(current_dir, import_module)

_dict_forms_lowercase = {ii.lower(): ii for ii in forms}
