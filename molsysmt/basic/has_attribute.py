# If digest is used in this method, other methods become slower

def has_attribute(molecular_system, attribute):

    from molsysmt import get_form
    from molsysmt.form import _dict_modules

    forms_in = get_form(molecular_system)

    if not isinstance(forms_in, (list, tuple)):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = False

    for form_in, item in zip(forms_in, molecular_system):
        if _dict_modules[form_in].has_attribute(item, attribute):
            output=True
            break
    
    return output

