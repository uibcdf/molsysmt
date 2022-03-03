from importlib import import_module
import os

forms = []

dict_type = {}
dict_info = {}
dict_attributes = {}
dict_is_form = {}
dict_extract = {}
dict_add = {}
dict_merge = {}
dict_append_structures = {}
dict_concatenate_structures = {}
dict_get = {}
dict_set = {}
dict_convert = {}

apis = []
file_apis = []
string_apis = []

current_dir = os.path.dirname(os.path.abspath(__file__))
apis = [filename.split('.')[0] for filename in os.listdir(current_dir) if filename.startswith('api_')]
file_apis = [filename.split('.')[0] for filename in os.listdir(current_dir) if filename.startswith('api_file_')]
string_apis = [filename.split('.')[0] for filename in os.listdir(current_dir) if filename.startswith('api_string_')]

for api_name in apis:

    mod = import_module('molsysmt.api_forms.'+api_name)

    forms.append(mod.form_name)

    dict_type[mod.form_name]=mod.form_type
    dict_info[mod.form_name]=mod.form_info
    dict_attributes[mod.form_name]=mod.form_attributes

    dict_is_form[mod.form_name]=mod.is_form
    dict_add[mod.form_name]=mod.add
    dict_merge[mod.form_name]=mod.merge
    dict_append_structures[mod.form_name]=mod.append_structures
    dict_concatenate_structures[mod.form_name]=mod.concatenate_structures
    dict_extract[mod.form_name]=mod.extract

    dict_convert[mod.form_name]= {}
    dict_get[mod.form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                          'entity':{}, 'system':{}, 'bond':{}}
    dict_set[mod.form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                          'entity':{}, 'system':{}, 'bond':{}}

    for method in mod.__dict__.keys():
        if method.startswith('to_'):
            if method.startswith('to_string_'):
                out_form_name=method.replace('to_string_','string:')
            elif method.startswith('to_file_'):
                out_form_name=method.replace('to_file_','file:')
            else:
                out_form_name=method.replace('to_','').replace('_','.',1)
            dict_convert[mod.form_name][out_form_name]= getattr(mod, method)
        if method.startswith('get_'):
            option, target = method[4:].split('_from_')
            dict_get[mod.form_name][target][option]=getattr(mod, method)
        if method.startswith('set_'):
            option, target = method[4:].split('_to_')
            dict_set[mod.form_name][target][option]=getattr(mod, method)

del(mod, method, out_form_name)
del(current_dir, import_module)

