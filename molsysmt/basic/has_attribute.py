from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

def has_attribute(molecular_system, attribute, check=True):

    if check:

        from molsysmt.tools.item import is_molecular_system
        from molsysmt.tools.attribute import is_attribute

        if not is_molecular_system(item):
            raise WrongItemError(attribute)

        if not is_attribute(attribute):
            raise WrongAttributeError(attribute)

    from molsysmt.tools.molecular_system import where_is_attribute

    output_item, output_form = where_is_attribute(item, attribute, check=False)

    output = False
    if output_item is not None:
        output = True

    return output

