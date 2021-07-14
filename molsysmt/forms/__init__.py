from importlib import import_module
import os
from molsysmt.forms.loader import api_to_be_loaded, converts_to_be_loaded, modules_detected

types = ['class', 'file', 'string', 'viewer']
forms = []

dict_type = {}
dict_is_form = {}
dict_info = {}
dict_add = {}
dict_append_frames = {}
dict_convert = {}
dict_get = {}
dict_set = {}
dict_has = {}
dict_extract_item = {}

file_extensions_recognized = []
string_names_recognized = []

current_dir = os.path.dirname(os.path.abspath(__file__))

for dirname, typename in [['classes', 'class'], ['files', 'file'], ['strings', 'string'], ['viewers', 'viewer']]:

    type_dir = os.path.join(current_dir, dirname)
    list_apis = [filename.split('.')[0] for filename in os.listdir(type_dir) if filename.startswith('api')]

    for api_name in list_apis:

        if api_to_be_loaded[api_name]:

            mod = import_module('molsysmt.forms.'+dirname+'.'+api_name)

            form_name = mod.form_name
            forms.append(form_name)

            dict_type[form_name]=typename
            dict_is_form.update(mod.is_form)
            dict_info[form_name]=mod.info
            dict_add[form_name]=mod.add
            dict_append_frames[form_name]=mod.append_frames
            dict_extract_item[form_name]=mod.extract_item

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
                            out_form_name=method.replace('to_','').replace('_',':')
                        elif method.startswith('to_file_'):
                            out_form_name=method.replace('to_','').replace('_',':')
                        else:
                            out_form_name=method.replace('to_','').replace('_','.')
                        dict_convert[form_name][out_form_name]= getattr(mod, method)
                if method.startswith('get_'):
                    option, target = method[4:].split('_from_')
                    dict_get[form_name][target][option]=getattr(mod, method)
                if method.startswith('set_'):
                    option, target = method[4:].split('_to_')
                    dict_set[form_name][target][option]=getattr(mod, method)

            del(mod, form_name)

    del(list_apis, type_dir, )

for aux_form_name in list(dict_is_form.keys()):
    if type(aux_form_name) is str:
        if aux_form_name.startswith('file:'):
            file_extensions_recognized.append(aux_form_name.split(':')[-1].lower())
        elif aux_form_name.startswith('string:'):
            string_names_recognized.append(aux_form_name.split(':')[-1])

del(import_module, dirname, typename)

