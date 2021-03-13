import numpy as np

def is_a_single_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has
    from molsysmt.molecular_system import MolecularSystem

    if type(items) in [list, tuple]:

        n_topologies=0
        n_coordinates=0
        n_topology_w_coordinates=0

        for item in items:

            if type(item) in [list, tuple, MolecularSystem]:
                return False
            else:
                form_in = get_form(item)
                has_topology = dict_has[form_in]["topology"]
                has_coordinates = dict_has[form_in]["coordinates"]
                has_box = dict_has[form_in]["box"]
                if has_topology:
                    n_topologies+=1
                if has_coordinates:
                    n_coordinates+=1
                    if has_topology:
                        n_topology_w_coordinates+=1

        if n_topologies>2 or n_coordinates>2:
            return False
        elif n_topologies==0:
            if n_coordinates<=1:
                return True
            else:
                return False
        elif n_topologies==1:
            if n_coordinates<=1:
                return True
            elif n_coordinates==2:
                if n_topology_w_coordinates==1:
                    return True
                else:
                    return False
            else:
                return False
        elif n_topologies==2:
            if n_coordinates==0:
                return False
            elif n_coordinates==1:
                if n_topology_w_coordinates==1:
                    return True
                else:
                    return False
            else:
                return False
    else:
        return True

def where_topology_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    topology_item = None
    topology_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_topology = dict_has[form_in]["topology"]
            has_coordinates = dict_has[form_in]["coordinates"]
            if has_topology:
                if topology_item is None:
                    topology_item = item
                    topology_form = form_in
                elif not has_coordinates:
                    topology_item = item
                    topology_form = form_in
    else:
        form_in = get_form(items)
        has_topology = dict_has[form_in]["topology"]
        if has_topology:
            topology_item = items
            topology_form = form_in

    return topology_item, topology_form

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
            has_topology = dict_has[form_in]["topology"]
            has_coordinates = dict_has[form_in]["coordinates"]
            if has_coordinates:
                if coordinates_item is None:
                    coordinates_item = item
                    coordinates_form = form_in
                elif not has_topology:
                    coordinates_item = item
                    coordinates_form = form_in
    else:
        form_in = get_form(items)
        has_coordinates = dict_has[form_in]["coordinates"]
        if has_coordinates:
            coordinates_item = items
            coordinates_form = form_in

    return coordinates_item, coordinates_form

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
            has_topology = dict_has[form_in]["topology"]
            has_coordinates = dict_has[form_in]["coordinates"]
            has_box = dict_has[form_in]["box"]
            if has_box and not (has_topology or has_coordinates):
                box_item = item
                box_form = form_in
                break
            else:
                if has_box:
                    if box_item is None:
                        box_item = item
                        box_form = form_in
                    elif not has_topology:
                        box_item = item
                        box_form = form_in
    else:
        form_in = get_form(items)
        has_box = dict_has[form_in]["box"]
        if has_box:
            box_item = items
            box_form = form_in

    return box_item, box_form

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
            has_topology = dict_has[form_in]["topology"]
            has_bonds = dict_has[form_in]["bonds"]
            if has_bonds and not has_topology:
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

def where_parameters_in_molecular_system(items):

    from molsysmt.multitool import get_form
    from molsysmt.forms import dict_has

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    parameters_item = None
    parameters_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_topology = dict_has[form_in]["topology"]
            has_parameters = dict_has[form_in]["parameters"]
            if has_parameters and not has_topology:
                parameterse_item = item
                parameters_form = form_in
                break
            else:
                if has_parameters:
                    if parameters_item is None:
                        parameters_item = item
                        parameters_form = form_in
    else:
        form_in = get_form(items)
        has_parameters = dict_has[form_in]["parameters"]
        if has_parameters:
            parameters_item = items
            parameters_form = form_in

    return parameters_item, parameters_form

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
            has_topology = dict_has[form_in]["topology"]
            has_parameters = dict_has[form_in]["parameters"]
            has_simulation = dict_has[form_in]["simulation"]
            if has_simulation and not (has_topology or has_parameters):
                simulation_item = item
                simulation_form = form_in
                break
            else:
                if has_simulation and has_parameters:
                    simulation_item = item
                    simulation_form = form_in
                    break
                else:
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

