from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def where_is_attribute(molecular_system, attribute=None):

    from molsysmt.basic.get_form import get_form
    from molsysmt.basic.is_a_molecular_system import is_a_molecular_system
    from molsysmt.basic.get.arguments import reverse_search, required_attributes
    from molsysmt.tools.attribute import is_attribute
    from molsysmt.api_forms import dict_attributes

    if not is_attribute(attribute):
        raise BadCallError('attribute')

    if not is_a_molecular_system(molecular_system):
        raise SingleMolecularSystemNeededError()

    if not is_list_or_tuple(molecular_system):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    if reverse_search[attribute]:
        aux_zip = zip(reversed(molecular_system), reversed(forms_in))
    else:
        aux_zip = zip(molecular_system, forms_in)

    output_item = None
    output_form = None

    for item, form_in in aux_zip:
        for required_attribute in required_attributes[attribute]:
            if dict_attributes[form_in][required_attribute]:
                output_item = item
                output_form = form_in
                break
        if output_form is not None:
            break

    return output_item, output_form

