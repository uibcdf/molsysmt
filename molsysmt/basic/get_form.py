from molsysmt.api_forms import dict_is_form
from molsysmt._private.lists_and_tuples import is_list_or_tuple
from molsysmt._private.exceptions import *

def get_form(molecular_system):

    # This method can check if molecular system is indeed a molecular system
    # This method is used to check that a molecular system is a molecular system

    if is_list_or_tuple(molecular_system):
        output = [get_form(ii) for ii in molecular_system]
        return output

    output = None

    for form, is_form in dict_is_form.items():
        if is_form(molecular_system):
            output = form
            break

    if output is None:
        raise NotSupportedFormError(type(output))

    return output

