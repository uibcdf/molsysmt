# If digest is used in this method, other methods become slower

def has_attribute(molecular_system, attribute):

    """
    Checking if a molecular system has a certain attribute.

    The function returns a dictionary with all attribute names as keys and True or False as values
    reporting whether or not the attribute is in the input molecular system.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be checked by the function.


    """

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

