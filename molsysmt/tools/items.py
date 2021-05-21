import numpy as np
import re as re
from .strings import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def compatibles_for_a_single_molecular_system(items):

    from molsysmt.multitool import get_form, get
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

    from molsysmt.multitool import get_form
    from molsysmt.multitool import dict_get

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

    from molsysmt.multitool import get_form
    from molsysmt.multitool import dict_get

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

    from molsysmt.multitool import get_form
    from molsysmt.multitool import dict_get

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

    from molsysmt.multitool import get_form
    from molsysmt.multitool import dict_get

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
            output = file_extension

    return output

def item_is_id(item):

    output = False

    if type(item) is not str:
        return output

    if len(item)==4 and item.isalnum():
        return 'PDB'

    return output

def item_is_string(item):

    output = False

    if type(item) is not str:
        return output

    if (' ' not in item) and ('\t' not in item) and ('\n' not in item):

        from molsysmt.elements.groups.aminoacid import name as aminoacid_name
        from molsysmt.elements.groups.water import name as water_name
        from molsysmt.elements.groups.aminoacid import aa1s

        if item.isalnum():

            # aminoacids3
            if len(item)%3==0:
                n_aa3 = 0
                aa3_list = re.findall('...', item)
                for aa3 in aa3_list:
                    if (aa3.upper() in aminoacid_name) or (aa3.upper() in water_name):
                        n_aa3+=1
                if (n_aa3*1.0)/(len(aa3_list)*1.0) > 0.8:
                    return 'aminoacids3'

            # aminoacids1
            n_aa1 = 0
            for aa1 in item:
                if (aa1.upper() in aa1s):
                        n_aa1+=1

            if (n_aa1*1.0)/(len(item)*1.0) > 0.8:
                return 'aminoacids1'

    else:

        if string_is_pdb(item):
            return 'pdb'

    return output

