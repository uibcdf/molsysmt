from molsysmt._private.digestion import digest

@digest()
def copy(molecular_system, output_filename=None):

    from . import get_form, is_a_molecular_system
    from molsysmt.item import is_file
    from molsysmt.api_forms import dict_extract

    form_in = get_form(molecular_system)

    if output_filename is None:

        if not isinstance(form_in, (list, tuple)):
            form_in = [form_in]
            molecular_system = [molecular_system]

        output = []

        for item_form, item in zip(form_in, molecular_system):
            output_item = dict_extract[item_form](item, copy_if_all=True)
            output.append(output_item)

        if len(output)==1:
            output=output[0]

    else:

        output = dict_extract[form_in](molecular_system, copy_if_all=True, output_filename=output_filename)

    return output

