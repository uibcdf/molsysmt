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

        for form_in in forms_in:
            for structural_attribute in structural_attributes:
                if structural_attribute in dict_attributes[form_in]:
                    if dict_attributes[form_in][structural_attribute]:
                        output = True
                        break
            if output:
                break


    elif attribute == 'topological':

        for form_in in forms_in:
            for topological_attribute in topological_attributes:
                if topological_attribute in dict_attributes[form_in]:
                    if dict_attributes[form_in][topological_attribute]:
                        output = True
                        break
            if output:
                break

    else:

        for form_in in forms_in:
            if dict_attributes[form_in][attribute]:
                output=True
                break
    
    return output

