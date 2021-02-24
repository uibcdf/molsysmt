from os import listdir as _listdir
from os.path import dirname as _dirname
from copy import deepcopy
from importlib import import_module as _import_module

def _not_implemented_conversion(item):
    raise NotImplementedError("This conversion has not been implemented yet")

list_api_forms=[filename.split('.')[0] for filename in _listdir(_dirname(__file__)) if filename.startswith('api')]

forms=[]
dict_api_forms={}
dict_convert={}
dict_select={}
dict_extract={}
dict_copy={}
dict_merge={}
dict_add={}
dict_append={}
dict_concatenate={}
dict_is_form={}
dict_get={}
dict_set={}
dict_info={}

for api_form in list_api_forms:
    module_api_form=_import_module('molsysmt.forms.seq.'+api_form,base_package)
    form_name=module_api_form.form_name
    forms.append(form_name)
    dict_api_forms[form_name]=module_api_form
    dict_is_form.update(module_api_form.is_form)

for form_name in forms:

    dict_convert[form_name]= {}
    dict_select[form_name]= {}
    dict_extract[form_name]= {}
    dict_copy[form_name]= {}
    dict_merge[form_name]= {}
    dict_add[form_name]= {}
    dict_append[form_name]= {}
    dict_concatenate[form_name]= {}
    dict_get[form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                          'entity':{}, 'system':{}, 'bond':{}}
    dict_set[form_name]= {'atom':{}, 'group':{}, 'component':{}, 'molecule':{}, 'chain':{},
                          'entity':{}, 'system':{}, 'bond':{}}
    dict_info[form_name]=getattr(dict_api_forms[form_name],'info')

    for method in dict_api_forms[form_name].__dict__.keys():
        if method.startswith('to_'):
            if method.endswith('_seq'):
                out_form_name=method[:-4].replace('to_','').replace('_','.')+':seq'
            elif method.endswith('_id'):
                out_form_name=method[:-3].replace('to_','').replace('_','.')+':id'
            else:
                out_form_name=method.replace('to_','').replace('_','.')
            dict_convert[form_name][out_form_name]= getattr(dict_api_forms[form_name],method)
        if method.startswith('select_with_'):
            syntaxis_name=method.replace('select_with_','')
            dict_select[form_name][syntaxis_name]= getattr(dict_api_forms[form_name],method)
        if method.startswith('get_'):
            option, target = method[4:].split('_from_')
            dict_get[form_name][target][option]=getattr(dict_api_forms[form_name], method)
        if method.startswith('set_'):
            option, target = method[4:].split('_to_')
            dict_set[form_name][target][option]=getattr(dict_api_forms[form_name], method)

    if 'extract' in dict_api_forms[form_name].__dict__.keys():
        dict_extract[form_name]=getattr(dict_api_forms[form_name],'extract')
    if 'copy' in dict_api_forms[form_name].__dict__.keys():
        dict_copy[form_name]=getattr(dict_api_forms[form_name],'copy')
    if 'merge' in dict_api_forms[form_name].__dict__.keys():
        dict_merge[form_name]=getattr(dict_api_forms[form_name],'merge')
    if 'add' in dict_api_forms[form_name].__dict__.keys():
        dict_add[form_name]=getattr(dict_api_forms[form_name],'add')
    if 'append' in dict_api_forms[form_name].__dict__.keys():
        dict_append[form_name]=getattr(dict_api_forms[form_name],'append')
    if 'concatenate' in dict_api_forms[form_name].__dict__.keys():
        dict_concatenate[form_name]=getattr(dict_api_forms[form_name],'concatenate')

forms=sorted(forms)

if 'out_form_name' in globals():
    del(out_form_name)
if 'syntaxis_name' in globals():
    del(syntaxis_name)

del(api_form, list_api_forms, form_name, module_api_form, base_package)

