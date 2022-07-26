from molsysmt._private.exceptions import NotSupportedFormError

def get_form(molecular_system):

    # This method can check if molecular system is indeed a molecular system
    # This method is used to check that a molecular system is a molecular system

    from molsysmt.api_forms import dict_is_form

    if isinstance(molecular_system, (list, tuple)):
        output = [get_form(ii) for ii in molecular_system]
        return output

    output = None

    for form, is_form in dict_is_form.items():
        if is_form(molecular_system):
            output = form
            break

    if output is None:
        raise NotSupportedFormError(type(output))

    return output

