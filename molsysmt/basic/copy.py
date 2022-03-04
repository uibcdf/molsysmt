from molsysmt._private_tools.exceptions import *
from molsysmt.tools.molecular_system import is_molecular_system
from molsysmt.tools.item import is_file

def copy(molecular_system, output_filename=None, check=False):

    if check:

        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

        if output_filename is not None:
            if not is_file(output_filename):
                raise WrongOutputFilenameError(output_filename)

    if output_filename is not None:

        raise NotImplementedMethodError()

    from molsysmt.basic import get_form

    form_in = get_form()

    if not is_list_or_tuple(get_form):
        form_in = [form_in]
        molecular_system = [molecular_system]

    output = []

    for item_form, item in zip(form_in, molecular_system):

        output_item = dict_extract[form_in](item, copy_if_all=True, check=False)
        output.append(output_item)

    if len(output)==1:
        output=output[0]

    return output

