# If digest is used in this method, other methods become slower

def get_attributes(molecular_system, output_type='dictionary'):

    from . import get_form
    from molsysmt.form import _dict_modules
    from molsysmt.attribute.attributes import attributes as _all_attributes

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    output = {ii:False for ii in _all_attributes}

    for form_in, item in zip(forms_in, molecular_system):
        for key, value in  _dict_modules[form_in].attributes.items():
            if value:
                output[key]=value

    if output_type=='dictionary':
        return output
    elif output_type=='list':
        return [ii for ii,jj in output.items() if jj]

