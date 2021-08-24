import numpy as np
import re as re
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def compatibles_for_a_single_molecular_system(items):

    from molsysmt.basic.get_form import get_form
    from molsysmt.basic.get import get
    from molsysmt.forms import dict_has

    output = True

    if not is_list_or_tuple(items):
        items=[items]

    if len(items)>1:

        list_n_atoms = []
        list_n_groups = []
        list_forms = []

        for item in items:
            tmp_form = get_form(item)
            tmp_n_atoms, tmp_n_groups = get(item, target='atom', n_atoms=True, n_groups=True)
            list_forms.append(tmp_form)
            list_n_atoms.append(tmp_n_atoms)
            list_n_groups.append(tmp_n_groups)

        Not_none_values = filter(None.__ne__, list_n_atoms)
        set_n_atoms = set(Not_none_values)
        if len(set_n_atoms)>1:
            output = False

        if output:

            Not_none_values = filter(None.__ne__, list_n_groups)
            set_n_groups = set(Not_none_values)
            if len(set_n_groups)>1:
                output = False

    return output

def has_topology(items):

    from molsysmt.basic import get_form
    from molsysmt.basic import dict_get

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_topology = dict_get[form_in]["system"]["has_topology"](item)
            output.append(w_topology)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_topology"](items)

    return output

def has_trajectory(items):

    from molsysmt.basic import get_form
    from molsysmt.basic import dict_get

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_trajectory = dict_get[form_in]["system"]["has_trajectory"](item)
            output.append(w_trajectory)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_trajectory"](items)

    return output

def has_coordinates(items):

    from molsysmt.basic import get_form
    from molsysmt.basic import dict_get

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
            output.append(w_coordinates)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_coordinates"](items)

    return output

def has_box(items):

    from molsysmt.basic import get_form
    from molsysmt.basic import dict_get

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_box = dict_get[form_in]["system"]["has_box"](item)
            output.append(w_box)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_box"](items)

    return output

def item_is_file(item):

    from molsysmt.forms import file_extensions_recognized

    output = False

    if type(item) is str:
        file_extension = item.split('.')[-1].lower()
        if file_extension in file_extensions_recognized:
            output = 'file:'+file_extension

    return output

def item_is_string(item):

    from molsysmt.forms import string_names_recognized
    from .strings import guess_form_from_string

    output = False

    if type(item) is str:
        if ':' in item:
            string_name = item.split(':')[0]
            if string_name in string_names_recognized:
                output = 'string:'+string_name
        if output==False:
            output = guess_form_from_string(item)
            if output is None:
                output = False

    return output


    return output

