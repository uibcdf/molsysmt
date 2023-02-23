from molsysmt._private.digestion import digest

@digest()
def where_is_attribute(molecular_system, attribute):

    from . import get_form
    from molsysmt.attribute.attributes import _required_attributes
    from molsysmt.api_forms import dict_attributes
    from molsysmt.attribute import is_topological_attribute

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    if not is_topological_attribute(attribute):
        aux_zip = zip(reversed(molecular_system), reversed(forms_in))
    else:
        aux_zip = zip(molecular_system, forms_in)

    output_item = None
    output_form = None

    for item, form_in in aux_zip:
        if dict_attributes[form_in][attribute]:
            output_item = item
            output_form = form_in
            break
        if output_form is not None:
            break

    return output_item, output_form

