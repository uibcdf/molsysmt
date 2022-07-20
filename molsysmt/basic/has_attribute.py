from molsysmt._private.digestion import digest
from molsysmt._private.lists_and_tuples import is_list_or_tuple

@digest
def has_attribute(molecular_system, attribute):

    from . import where_is_attribute

    output_item, output_form = where_is_attribute(molecular_system, attribute)

    output = False
    if output_item is not None:
        output = True

    return output

