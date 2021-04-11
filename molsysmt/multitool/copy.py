from molsysmt.forms import dict_copy
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *

def copy(molecular_system, output_filename=None):

    output = []

    molecular_system = digest_molecular_system(molecular_system)
    items, forms = molecular_system.get_items()

    if output_filename is None:
        for item, form_in in zip(items, forms):
            tmp_item = dict_copy[form_in](item)
            output.append(tmp_item)
    else:
        if not is_list_or_tuple(output_filename):
            output_filename = [output_filename]
        for item, form_in, aux_filename in zip(items, forms, output_filename):
            tmp_item = dict_copy[form_in](item, output_filename=aux_filename)
            output.append(tmp_item)

    output = digest_output(output)

    return output

