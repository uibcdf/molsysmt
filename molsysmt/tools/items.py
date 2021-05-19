import numpy as np
import re as re
from .strings import *

def compatibles_for_a_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.multitool import dict_get

    compatible = True

    n_atoms = None
    atom_names = None

    if not is_a_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            w_topology = dict_get[form_in]["system"]["has_topology"](item)
            w_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
            if w_topology:
                aux_n_atoms = dict_get[form_in]["system"]["n_atoms"](item)
                aux_atom_names = dict_get[form_in]["atom"]["atom_name"](item)
                if n_atoms is None:
                    n_atoms = aux_n_atoms
                elif n_atoms != aux_n_atoms:
                    compatible=False
                    break
                if atom_names is None:
                    atom_names = aux_atom_names
                elif atom_names != aux_atom_names:
                    compatible=False
                    break
            if w_coordinates:
                aux_n_atoms = dict_get[form_in]["system"]["n_atoms"](item)
                if n_atoms is None:
                    n_atoms = aux_n_atoms
                elif n_atoms != aux_n_atoms:
                    compatible=False
                    break

    return compatible

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
        filename_decomposition = item.split('.')
        if len(filename_decomposition)==2:
            file_extension = filename_decomposition[1].lower()
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

