from importlib import import_module
import os

types = ['class', 'file', 'id', 'seq', 'viewer']
forms = []

dict_type = {}
dict_is_form = {}
dict_info = {}
dict_extract = {}
dict_copy = {}
dict_merge = {}
dict_add = {}
dict_append = {}
dict_concatenate = {}
dict_convert = {}
dict_select = {}
dict_get = {}
dict_set = {}

current_dir = os.path.dirname(os.path.abspath(__file__))

for dirname, typename in [['classes', 'class'], ['files', 'file'], ['ids', 'id'], ['seqs', 'seq'], ['viewers', 'viewer']]:

    type_dir = os.path.join(current_dir, dirname)
    list_apis = [filename.split('.')[0] for filename in os.listdir(type_dir) if filename.startswith('api')]

    for api_name in list_apis:

        mod = import_module('molsysmt.forms.'+dirname+'.'+api_name)

        form_name = mod.form_name
        forms.append(form_name)

        dict_type[form_name]=typename
        dict_is_form.update(mod.is_form)
        dict_info[form_name]=mod.info
        dict_extract[form_name]=mod.extract
        dict_copy[form_name]=mod.copy
        dict_merge[form_name]=mod.merge
        dict_add[form_name]=mod.add
        dict_append[form_name]=mod.append
        dict_concatenate[form_name]=mod.concatenate

        dict_convert[form_name]= {}
        dict_select[form_name]= {}
        dict_get[form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                              'entity':{}, 'system':{}, 'bond':{}}
        dict_set[form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                              'entity':{}, 'system':{}, 'bond':{}}

        for method in mod.__dict__.keys():
            if method.startswith('to_'):
                if method.endswith('_seq'):
                    out_form_name=method[:-4].replace('to_','').replace('_','.')+':seq'
                elif method.endswith('_id'):
                    out_form_name=method[:-3].replace('to_','').replace('_','.')+':id'
                else:
                    out_form_name=method.replace('to_','').replace('_','.')
                dict_convert[form_name][out_form_name]= getattr(mod, method)
            if method.startswith('select_with_'):
                syntaxis_name=method.replace('select_with_','')
                dict_select[form_name][syntaxis_name]= getattr(mod, method)
            if method.startswith('get_'):
                option, target = method[4:].split('_from_')
                dict_get[form_name][target][option]=getattr(mod, method)
            if method.startswith('set_'):
                option, target = method[4:].split('_to_')
                dict_set[form_name][target][option]=getattr(mod, method)

        del(mod, form_name)

    del(list_apis, type_dir, )

del(import_module, dirname, typename)

