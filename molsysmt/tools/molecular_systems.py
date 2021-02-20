import numpy as np

def is_a_single_molecular_system(items):

    from molsysmt import get_form
    from molsysmt.multitool import dict_get

    if type(items) in [list, tuple]:

        n_topologies=0
        n_coordinates=0
        n_topology_w_coordinates=0

        for item in items:

            if type(item) in [list, tuple]:
                return False
            else:
                form_in = get_form(item)
                has_topology = dict_get[form_in]["system"]["has_topology"](item)
                has_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
                has_box = dict_get[form_in]["system"]["has_box"](item)
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

    from molsysmt import get_form
    from molsysmt.multitool import dict_get

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    topology_item = None
    topology_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_topology = dict_get[form_in]["system"]["has_topology"](item)
            has_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
            if has_topology:
                if topology_item is None:
                    topology_item = item
                    topology_form = form_in
                elif not has_coordinates:
                    topology_item = item
                    topology_form = form_in
    else:
        form_in = get_form(items)
        has_topology = dict_get[form_in]["system"]["has_topology"](items)
        if has_topology:
            topology_item = items
            topology_form = form_in

    return topology_item, topology_form

def where_coordinates_in_molecular_system(items):

    from molsysmt import get_form
    from molsysmt.multitool import dict_get

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    coordinates_item = None
    coordinates_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_topology = dict_get[form_in]["system"]["has_topology"](item)
            has_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
            if has_coordinates:
                if coordinates_item is None:
                    coordinates_item = item
                    coordinates_form = form_in
                elif not has_topology:
                    coordinates_item = item
                    coordinates_form = form_in
    else:
        form_in = get_form(items)
        has_coordinates = dict_get[form_in]["system"]["has_coordinates"](items)
        if has_coordinates:
            coordinates_item = items
            coordinates_form = form_in

    return coordinates_item, coordinates_form

def where_trajectory_in_molecular_system(items):

    from molsysmt import get_form
    from molsysmt.multitool import dict_get

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    trajectory_item = None
    trajectory_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_topology = dict_get[form_in]["system"]["has_topology"](item)
            has_trajectory = dict_get[form_in]["system"]["has_trajectory"](item)
            if has_trajectory:
                if trajectory_item is None:
                    trajectory_item = item
                    trajectory_form = form_in
                elif not has_topology:
                    trajectory_item = item
                    trajectory_form = form_in
    else:
        form_in = get_form(items)
        has_trajectory = dict_get[form_in]["system"]["has_coordinates"](items)
        if has_trajectory:
            trajectory_item = items
            trajectory_form = form_in

    return trajectory_item

def where_box_in_molecular_system(items):

    from molsysmt import get_form
    from molsysmt.multitool import dict_get

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    box_item = None
    box_form = None

    if type(items) in [list, tuple]:
        for item in items:
            form_in = get_form(item)
            has_topology = dict_get[form_in]["system"]["has_topology"](item)
            has_coordinates = dict_get[form_in]["system"]["has_coordinates"](item)
            has_box = dict_get[form_in]["system"]["has_box"](item)
            if has_box and not (has_topology or has_coordinates):
                box_item = item
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
        has_box = dict_get[form_in]["system"]["has_box"](items)
        if has_box:
            box_item = items
            box_form = form_in

    return box_item, box_form

