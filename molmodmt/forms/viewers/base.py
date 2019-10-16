from os import listdir as _listdir
from os.path import dirname as _dirname
from copy import deepcopy
from importlib import import_module as _import_module
from .get_fields import target_fields as get_target_dict
from .set_fields import target_fields as set_target_dict

base_package = __name__.replace('.base','')

def _not_implemented_conversion(item):
    raise NotImplementedError("This conversion has not been implemented yet")

list_api_forms=[filename.split('.')[0] for filename in _listdir(_dirname(__file__)) if filename.startswith('api')]

dict_api_forms={}
list_forms=[]
dict_converter={}
dict_selector={}
dict_extractor={}
dict_duplicator={}
dict_merger={}
dict_is_form={}
dict_get={}
dict_set={}

for api_form in list_api_forms:
    module_api_form=_import_module('.'+api_form,base_package)
    form_name=module_api_form.form_name
    list_forms.append(form_name)
    dict_api_forms[form_name]=module_api_form
    dict_is_form.update(module_api_form.is_form)

for form_name in list_forms:

    dict_converter[form_name]= {}
    dict_selector[form_name]= {}
    dict_extractor[form_name]= {}
    dict_duplicator[form_name]= {}
    dict_merger[form_name]= {}
    dict_get[form_name]= deepcopy(get_target_dict)
    dict_set[form_name]= deepcopy(set_target_dict)

    for method in dict_api_forms[form_name].__dict__.keys():
        if method.startswith('to_'):
            if method.endswith('_seq'):
                out_form_name=method[:-4].replace('to_','').replace('_','.')+':seq'
            elif method.endswith('_id'):
                out_form_name=method[:-3].replace('to_','').replace('_','.')+':id'
            else:
                out_form_name=method.replace('to_','').replace('_','.')
            dict_converter[form_name][out_form_name]= getattr(dict_api_forms[form_name],method)
        if method.startswith('select_with_'):
            syntaxis_name=method.replace('select_with_','')
            dict_selector[form_name][syntaxis_name]= getattr(dict_api_forms[form_name],method)

    if 'extract_subsystem' in dict_api_forms[form_name].__dict__.keys():
        dict_extractor[form_name]=getattr(dict_api_forms[form_name],'extract_subsystem')
    if 'duplicate' in dict_api_forms[form_name].__dict__.keys():
        dict_duplicator[form_name]=getattr(dict_api_forms[form_name],'duplicate')
    if 'merge_two_items' in dict_api_forms[form_name].__dict__.keys():
        dict_merger[form_name]=getattr(dict_api_forms[form_name],'merge_two_items')

    for target in dict_get[form_name]:
        for option in dict_get[form_name][target]:
            get_function_name = 'get_'+option+'_from_'+target
            if get_function_name in dict_api_forms[form_name].__dict__.keys():
                dict_get[form_name][target][option]=getattr(dict_api_forms[form_name],get_function_name)

    for target in dict_set[form_name]:
        for option in dict_set[form_name][target]:
            set_function_name = 'set_'+option+'_to_'+target
            if set_function_name in dict_api_forms[form_name].__dict__.keys():
                dict_set[form_name][target][option]=getattr(dict_api_forms[form_name],set_function_name)



list_forms=sorted(list_forms)

if 'out_form_name' in globals():
    del(out_form_name)
if 'syntaxis_name' in globals():
    del(syntaxis_name)

del(api_form, list_api_forms, form_name, module_api_form, base_package)
del(get_target_dict, set_target_dict)

