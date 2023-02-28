from molsysmt._private.digestion import digest

@digest()
def has_attribute(molecular_system, attribute):

    from molsysmt import get_form
    from molsysmt.api_forms import dict_attributes
    from molsysmt.attribute.attributes import topological_attributes, structural_attributes,\
            mechanical_attributes

    forms_in = get_form(molecular_system)

    if not isinstance(forms_in, (list, tuple)):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = False

    if attribute == 'structural': 

        for form_in, item in zip(forms_in, molecular_system):
            if form_in in ['molsysmt.MolecularMechanicsDict', 'molsysmt.StructuresDict']:
                for structural_attribute in structural_attributes:
                    if structural_attribute in item:
                        output = True
                        break
            else:
                for structural_attribute in structural_attributes:
                    if structural_attribute in dict_attributes[form_in]:
                        if dict_attributes[form_in][structural_attribute]:
                            output = True
                            break
            if output:
                break

    elif attribute == 'topological':

        for form_in, item in zip(forms_in, molecular_system):
            if form_in in ['molsysmt.MolecularMechanicsDict', 'molsysmt.StructuresDict']:
                for topological_attribute in topological_attributes:
                    if topological_attribute in item:
                        output = True
                        break
            else:
                for topological_attribute in topological_attributes:
                    if topological_attribute in dict_attributes[form_in]:
                        if dict_attributes[form_in][topological_attribute]:
                            output = True
                            break
            if output:
                break

    elif attribute == 'mechanical':

        for form_in, item in zip(forms_in, molecular_system):
            if form_in in ['molsysmt.MolecularMechanicsDict', 'molsysmt.StructuresDict']:
                for mechanical_attribute in mechanical_attributes:
                    if mechanical_attribute in item:
                        output = True
                        break
            else:
                for mechanical_attribute in mechanical_attributes:
                    if mechanical_attribute in dict_attributes[form_in]:
                        if dict_attributes[form_in][mechanical_attribute]:
                            output = True
                            break
            if output:
                break

    else:

        for form_in, item in zip(forms_in, molecular_system):
            if form_in in ['molsysmt.MolecularMechanicsDict', 'molsysmt.StructuresDict']:
                if attribute in item:
                    output=True
            elif dict_attributes[form_in][attribute]:
                output=True
    
    return output

