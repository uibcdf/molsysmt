from molsysmt._private.digestion import digest

@digest()
def has_attribute(molecular_system, attribute):

    from molsysmt import get_form
    from molsysmt.api_forms import dict_attributes
    from molsysmt.attribute.attributes import topological_attributes, structural_attributes

    forms_in = get_form(molecular_system)

    if not isinstance(forms_in, (list, tuple)):
        forms_in = [forms_in]

    output = False

    if attribute == 'structural': 

        for ii in structural_attributes:
            for form_in in forms_in:



    elif attribute == 'topological':



    else:

        for form_in in forms_in:
            if attribute in dict_attributes[]
    
        from . import where_is_attribute

        output_item, output_form = where_is_attribute(molecular_system, attribute)

        output = False
        if output_item is not None:
            output = True

    return output

