from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.lists_and_tuples import is_list_or_tuple

# TODO: this function has unresolved references. Also, variable item is not defined anywhere.
def has_attribute(molecular_system, attribute, check=True):

    from . import where_is_attribute, is_molecular_system
    from molsysmt.tools.attribute import is_attribute

    if check:

        if not is_molecular_system(item):
            raise WrongItemError(attribute)

        if not is_attribute(attribute):
            raise WrongAttributeError(attribute)

    output_item, output_form = where_is_attribute(item, attribute, check=False)

    output = False
    if output_item is not None:
        output = True

    return output

