from importlib import import_module
import os

list_is_file_form = []
current_dir = os.path.dirname(os.path.abspath(__file__))

for dirname in os.listdir(current_dir):
    if dirname.startswith('file_'):
        form_name = dirname
        mod = import_module('molsysmt.form.'+dirname)
        list_is_file_form.append(getattr(mod, 'is_'+form_name))

# This method must not be digested
def is_file(form):

    output = False

    for is_file_form in list_is_file_form:
        if is_file_form(form):
            output = True
            break

    return output

