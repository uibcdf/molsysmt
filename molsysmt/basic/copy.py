from molsysmt._private.digestion import digest

@digest()
def copy(molecular_system, output_filename=None):

    from . import get_form
    from molsysmt.form import is_file, _dict_modules

    form_in = get_form(molecular_system)

    if output_filename is None:

        if not isinstance(form_in, (list, tuple)):
            form_in = [form_in]
            molecular_system = [molecular_system]

        output = []

        for item_form, item in zip(form_in, molecular_system):
            output_item = _dict_modules[item_form].copy(item)
            output.append(output_item)

        if len(output)==1:
            output=output[0]

    else:

        output = _dict_modules[form_in].copy(molecular_system, output_filename=output_filename)

    return output

