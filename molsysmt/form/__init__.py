from .is_item import is_item
from .is_file import is_file
from .is_string import is_string

import os
from importlib import import_module

_dict_modules={}

current_dir = os.path.dirname(os.path.abspath(__file__))
for f in os.scandir(current_dir):
    if f.is_dir() and f.name not in ['__pycache__']:
        mod = import_module('molsysmt.form.'+f.name)
        _dict_modules[mod.form_name] = mod

_dict_forms_lowercase = {ii.lower(): ii for ii in _dict_modules.keys()}

del(current_dir, os, mod, f)

