from molsysmt._private.exceptions import NotSupportedFormError

# This method must not be digested
def get_form(molecular_system):

    # This method can check if molecular system is indeed a molecular system
    # This method is used to check that a molecular system is a molecular system

    from molsysmt.form import _dict_modules

    if isinstance(molecular_system, (list, tuple)):
        output = [get_form(ii) for ii in molecular_system]
        return output

    output = None

    for form, module in _dict_modules.items():
        if module.is_form(molecular_system):
            output = form
            break

    if output is None:
        raise NotSupportedFormError(type(molecular_system))

    return output

