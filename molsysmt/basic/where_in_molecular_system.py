from molsysmt._private_tools.exceptions import *

def where_in_molecular_system(molecular_system, attribute=None):

    from molsysmt.basic.get_form import get_form
    from molsysmt.forms import dict_has

    if attribute not in ['elements', 'bonds', 'coordinates']:

        pass

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    output_item = None
    output_form = None

    if attribute=='elements':

        if is_list_or_tuple(items):
            for item in items:
                form_in = get_form(item)
                has_elements = dict_has[form_in]["elements"]
                has_coordinates = dict_has[form_in]["coordinates"]
                if has_elements:
                    if elements_item is None:
                        output_item = item
                        output_form = form_in
                    elif not has_coordinates:
                        output_item = item
                        output_form = form_in
        else:
            form_in = get_form(items)
            has_elements = dict_has[form_in]["elements"]
            if has_elements:
                output_item = items
                output_form = form_in

    elif attribute=='bonds':



def _where_bonds(items):

    from molsysmt.basic.get_form import get_form
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

def _where_coordinates(items):

    from molsysmt.basic.get_form import get_form
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


