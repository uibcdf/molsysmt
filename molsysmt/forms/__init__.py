from importlib import import_module

types = ['class', 'file', 'id', 'seq', 'viewer']
forms = []

dict_type = {}
dict_is_form = {}
dict_info = {}
dict_convert = {}
dict_select = {}
dict_extract = {}
dict_copy = {}
dict_merge = {}
dict_add = {}
dict_append = {}
dict_concatenate = {}
dict_get = {}
dict_set = {}

for module, type in [['classes', 'class'], ['files', 'file'], ['ids', 'id'], ['seqs', 'seq'], ['viewers', 'viewer']]:

    mod = import_module('molsysmt.forms.'+module)

    forms+=mod.forms
    for form in mod.forms:
        dict_type[form]=type

    dict_is_form.update(mod.dict_is_form)
    dict_info.update(mod.dict_info)
    dict_convert.update(mod.dict_convert)
    dict_select.update(mod.dict_select)
    dict_extract.update(mod.dict_extract)
    dict_copy.update(mod.dict_copy)
    dict_merge.update(mod.dict_merge)
    dict_add.update(mod.dict_add)
    dict_concatenate.update(mod.dict_concatenate)
    dict_append.update(mod.dict_append)
    dict_get.update(mod.dict_get)
    dict_set.update(mod.dict_set)

    del(mod)

del(import_module)

