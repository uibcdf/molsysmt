import numpy as np
from molsysmt._private_tools.exceptions import *
from molsysmt.tools.items import compatibles_for_a_single_molecular_system as items_compatibles_for_a_single_molecular_system
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def is_a_single_molecular_system(items):

    if is_list_or_tuple(items):
        for item in items:
            if is_list_or_tuple(item):
                return False

    output = items_compatibles_for_a_single_molecular_system(items)

    return output

def where_elements_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    elements_item = None
    elements_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_coordinates = dict_has[form_in]["coordinates"]
            if has_elements:
                if elements_item is None:
                    elements_item = item
                    elements_form = form_in
                elif not has_coordinates:
                    elements_item = item
                    elements_form = form_in
    else:
        form_in = get_form(items)
        has_elements = dict_has[form_in]["elements"]
        if has_elements:
            elements_item = items
            elements_form = form_in

    return elements_item, elements_form

def where_bonds_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    bonds_item = None
    bonds_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_bonds = dict_has[form_in]["bonds"]
            if has_bonds and not has_elements:
                bonds_item = item
                bonds_form = form_in
                break
            else:
                if has_bonds:
                    if bonds_item is None:
                        bonds_item = item
                        bonds_form = form_in
    else:
        form_in = get_form(items)
        has_bonds = dict_has[form_in]["bonds"]
        if has_bonds:
            bonds_item = items
            bonds_form = form_in

    return bonds_item, bonds_form

def where_coordinates_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    coordinates_item = None
    coordinates_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_coordinates = dict_has[form_in]["coordinates"]
            if has_coordinates:
                if coordinates_item is None:
                    coordinates_item = item
                    coordinates_form = form_in
                elif not has_elements:
                    coordinates_item = item
                    coordinates_form = form_in
    else:
        form_in = get_form(items)
        has_coordinates = dict_has[form_in]["coordinates"]
        if has_coordinates:
            coordinates_item = items
            coordinates_form = form_in

    return coordinates_item, coordinates_form

def where_velocities_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    velocities_item = None
    velocities_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_velocities = dict_has[form_in]["velocities"]
            if has_velocities:
                if velocities_item is None:
                    velocities_item = item
                    velocities_form = form_in
                elif not has_elements:
                    velocities_item = item
                    velocities_form = form_in
    else:
        form_in = get_form(items)
        has_velocities = dict_has[form_in]["velocities"]
        if has_velocities:
            velocities_item = items
            velocities_form = form_in

    return velocities_item, velocities_form

def where_box_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    box_item = None
    box_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_coordinates = dict_has[form_in]["coordinates"]
            has_box = dict_has[form_in]["box"]
            if has_box and not (has_elements or has_coordinates):
                box_item = item
                box_form = form_in
                break
            else:
                if has_box:
                    if box_item is None:
                        box_item = item
                        box_form = form_in
                    elif not has_elements:
                        box_item = item
                        box_form = form_in
    else:
        form_in = get_form(items)
        has_box = dict_has[form_in]["box"]
        if has_box:
            box_item = items
            box_form = form_in

    return box_item, box_form

def where_ff_parameters_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    ff_parameters_item = None
    ff_parameters_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_ff_parameters = dict_has[form_in]["ff_parameters"]
            if has_ff_parameters and not has_elements:
                ff_parameters_item = item
                ff_parameters_form = form_in
                break
            else:
                if has_ff_parameters:
                    if ff_parameters_item is None:
                        ff_parameters_item = item
                        ff_parameters_form = form_in
    else:
        form_in = get_form(items)
        has_ff_parameters = dict_has[form_in]["ff_parameters"]
        if has_ff_parameters:
            ff_parameters_item = items
            ff_parameters_form = form_in

    return ff_parameters_item, ff_parameters_form

def where_mm_parameters_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    mm_parameters_item = None
    mm_parameters_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_ff_parameters = dict_has[form_in]["ff_parameters"]
            has_mm_parameters = dict_has[form_in]["mm_parameters"]
            if has_mm_parameters and not (has_elements or has_ff_parameters):
                mm_parameters_item = item
                mm_parameters_form = form_in
                break
            else:
                if has_mm_parameters and has_ff_parameters:
                    mm_parameters_item = item
                    mm_parameters_form = form_in
                    break
                elif has_mm_parameters:
                    if mm_parameters_item is None:
                        mm_parameters_item = item
                        mm_parameters_form = form_in

    else:
        form_in = get_form(items)
        has_mm_parameters = dict_has[form_in]["mm_parameters"]
        if has_mm_parameters:
            mm_parameters_item = items
            mm_parameters_form = form_in

    return mm_parameters_item, mm_parameters_form

def where_simulation_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    simulation_item = None
    simulation_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_simulation = dict_has[form_in]["simulation"]
            if has_simulation and not has_elements:
                simulation_item = item
                simulation_form = form_in
                break
            else:
                if has_simulation:
                    if simulation_item is None:
                        simulation_item = item
                        simulation_form = form_in
    else:
        form_in = get_form(items)
        has_simulation = dict_has[form_in]["simulation"]
        if has_simulation:
            simulation_item = items
            simulation_form = form_in

    return simulation_item, simulation_form

def where_thermo_state_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    thermo_state_item = None
    thermo_state_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_simulation = dict_has[form_in]["simulation"]
            has_thermo_state = dict_has[form_in]["thermo_state"]
            if has_thermo_state and not (has_elements or has_simulation):
                thermo_state_item = item
                thermo_state_form = form_in
                break
            else:
                if has_thermo_state and has_simulation:
                    thermo_state_item = item
                    thermo_state_form = form_in
                    break
                elif has_thermo_state:
                    if thermo_state_item is None:
                        thermo_state_item = item
                        thermo_state_form = form_in

    else:
        form_in = get_form(items)
        has_thermo_state = dict_has[form_in]["thermo_state"]
        if has_thermo_state:
            thermo_state_item = items
            thermo_state_form = form_in

    return thermo_state_item, thermo_state_form

