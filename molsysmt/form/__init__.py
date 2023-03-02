from .is_item import is_item
from .is_file import is_file
from .is_string import is_string

import os
from importlib import import_module

_dict={}
_dict_convert={}

current_dir = os.path.dirname(os.path.abspath(__file__))
for f in os.scandir(current_dir):
    if f.is_dir() and f.name not in ['__pycache__']:
        mod = import_module('molsysmt.form.'+f.name)
        _dict[mod.form_name] = mod
        _dict_convert[mod.form_name] = mod._dict_convert

del(current_dir, os, mod, f)

