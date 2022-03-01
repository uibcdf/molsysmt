from molsysmt._private_tools.exceptions import *

def where_is_attribute(molecular_system, attribute=None):

    from molsysmt.basic.get_form import get_form
    from molsysmt.basic.is_a_molecular_system import is_a_molecular_system
    from molsysmt.api_forms import dict_has
    from molsysmt.tools import is_attribute

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input")

    output_item = None
    output_form = None

    if not is_list_or_tuple(items):
        items = [items]

    if attribute=='elements':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_coordinates = dict_has[form_in]["coordinates"]
            if has_elements:
                if output_item is None:
                    output_item = item
                    output_form = form_in
                elif not has_coordinates:
                    output_item = item
                    output_form = form_in

    elif attribute=='bonds':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_bonds = dict_has[form_in]["bonds"]
            if has_bonds and not has_elements:
                output_item = item
                output_form = form_in
                break
            else:
                if has_bonds:
                    if output_item is None:
                        output_item = item
                        output_form = form_in

    elif attribute=='coordinates':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_coordinates = dict_has[form_in]["coordinates"]
            if has_coordinates:
                if output_item is None:
                    output_item = item
                    output_form = form_in
                elif not has_elements:
                    output_item = item
                    output_form = form_in

    elif attribute=='velocities':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_velocities = dict_has[form_in]["velocities"]
            if has_velocities:
                if output_item is None:
                    output_item = item
                    output_form = form_in
                elif not has_elements:
                    output_item = item
                    output_form = form_in

    elif attribute=='box':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_coordinates = dict_has[form_in]["coordinates"]
            has_box = dict_has[form_in]["box"]
            if has_box and not (has_elements or has_coordinates):
                output_item = item
                output_form = form_in
                break
            else:
                if has_box:
                    if output_item is None:
                        output_item = item
                        output_form = form_in
                    elif not has_elements:
                        output_item = item
                        output_form = form_in

    elif attribute=='ff_parameters':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_ff_parameters = dict_has[form_in]["ff_parameters"]
            if has_ff_parameters and not has_elements:
                output_item = item
                output_form = form_in
                break
            else:
                if has_ff_parameters:
                    if output_item is None:
                        output_item = item
                        output_form = form_in

    elif attribute=='mm_parameters':

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

    elif attribute=='simulation':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_simulation = dict_has[form_in]["simulation"]
            if has_simulation and not has_elements:
                output_item = item
                output_form = form_in
                break
            else:
                if has_simulation:
                    if output_item is None:
                        output_item = item
                        output_form = form_in

    elif attribute=='thermo_state':

        for item in items:
            form_in = get_form(item)
            has_elements = dict_has[form_in]["elements"]
            has_simulation = dict_has[form_in]["simulation"]
            has_thermo_state = dict_has[form_in]["thermo_state"]
            if has_thermo_state and not (has_elements or has_simulation):
                output_item = item
                output_form = form_in
                break
            else:
                if has_thermo_state and has_simulation:
                    output_item = item
                    output_form = form_in
                    break
                elif has_thermo_state:
                    if output_item is None:
                        output_item = item
                        output_form = form_in

    else:

        raise ValueError ("Invalid value of input argument 'attribute'.")

    return output_item, output_form

