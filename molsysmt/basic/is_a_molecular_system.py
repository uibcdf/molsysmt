import numpy as np
from molsysmt._private_tools.exceptions import *
from molsysmt.tools.items import compatibles_for_a_single_molecular_system as items_compatibles_for_a_single_molecular_system
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def is_a_molecular_system(items):

    if is_list_or_tuple(items):
        for item in items:
            if is_list_or_tuple(item):
                return False

    output = items_compatibles_for_a_single_molecular_system(items)


    if output:

        if is_list_or_tuple(items):

            if len(items)>1:

                from molsysmt.basic import get_form
                from molsysmt.forms import dict_has

                with_elements_and_coordinates=0
                for item in items:
                    form_in = get_form(item)
                    has_elements = dict_has[form_in]["elements"]
                    has_coordinates = dict_has[form_in]["coordinates"]
                    if has_elements and has_coordinates:
                        with_elements_and_coordinates+=1

                if with_elements_and_coordinates>1:
                    output = False

    return output

