import numpy as np
from molsysmt import get_form
from molsysmt.multitool import dict_get

def compatibles_for_a_molecular_system(items):

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

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_topology = dict_get[form_in]["system"]["has_topology"](item)
            output.append(w_topology)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_topology"](item)

    return output

def has_trajectory(items):

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_trajectory = dict_get[form_in]["system"]["has_trajectory"](item)
            output.append(w_trajectory)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_trajectory"](item)

    return output

def has_coordinates(items):

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
            output.append(w_coordinates)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_coordinates"](item)

    return output

def has_box(items):

    if type(items) in [list, tuple]:
        output = []
        for item in items:
            form_in = get_form(item)
            w_box = dict_get[form_in]["system"]["has_box"](item)
            output.append(w_box)
    else:
        form_in = get_form(items)
        output = dict_get[form_in]["system"]["has_box"](item)

    return output


