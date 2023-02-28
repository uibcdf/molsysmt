from .is_item import is_item
from .is_file import is_file
from .is_string import is_string

import os
from importlib import import_module

current_dir = os.path.dirname(os.path.abspath(__file__))
for dirname in os.listdir(current_dir):
    if os.path.isdir(dirname) and dirname!='__pycache__':

        import_module('molsysmt.form.'+dirname)
        
del(os, import_module, current_dir, dirname)
