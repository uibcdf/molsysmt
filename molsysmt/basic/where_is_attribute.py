from molsysmt._private.digestion import digest

@digest()
def where_is_attribute(molecular_system, attribute, digest=False):

    from . import get_form, is_a_molecular_system
    from molsysmt.attribute.attributes import _reverse_search_in_molecular_system, _required_attributes
    from molsysmt.api_forms import dict_attributes
    from molsysmt.attribute import is_attribute

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    if _reverse_search_in_molecular_system[attribute]:
        aux_zip = zip(reversed(molecular_system), reversed(forms_in))
    else:
        aux_zip = zip(molecular_system, forms_in)

    output_item = None
    output_form = None

    for item, form_in in aux_zip:
        for required_attribute in _required_attributes[attribute]:
            if dict_attributes[form_in][required_attribute]:
                output_item = item
                output_form = form_in
                break
        if output_form is not None:
            break

    return output_item, output_form

