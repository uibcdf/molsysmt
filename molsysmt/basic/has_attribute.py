from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def has_attribute(molecular_system, attribute):

    from molsysmt.basic.get_form import get_form
    from molsysmt.basic.is_a_molecular_system import is_a_molecular_system
    from molsysmt.tools import is_attribute
    from molsysmt.api_forms import dict_has
    from molsysmt._private_tools.output import digest_output

    attributes = attribute
    if not is_list_or_tuple(attributes):
        attributes = [attributes]

    for attribute in attributes:
        if not is_attribute(attribute):
            raise ValueError ("The input argument {} is not an attribute.".format(attribute))

    if not is_list_or_tuple(molecular_system):
        molecular_system = [molecular_system]

    if not is_a_single_molecular_system(items):
        raise ValueError ("This method needs a single molecular system as input.")

    output = []

    for item in molecular_system:

        form_in = get_form(item)

        for attribute in attributes:

            output.append(dict_has[form_in][attribute])


    output = digest_output(output)

    return output

