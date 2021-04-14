from molsysmt import puw
from molsysmt.forms import dict_is_form
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import digest_output
from molsysmt._private_tools.forms import to_form_is_file, form_is_file, form_of_file, are_equal_sets_of_forms
from molsysmt.molecular_system import MolecularSystem
from molsysmt._private_tools.exceptions import *

def get_form(molecular_system):

    if type(molecular_system)==MolecularSystem:
        _, output = molecular_system.get_items()
        output = digest_output(output)
        return output

    if puw.is_quantity(molecular_system):

        from molsysmt.forms.classes.api_XYZ import this_Quantity_is_XYZ
        from molsysmt.forms.classes.api_XYZ import form_name as form_XYZ

        if this_Quantity_is_XYZ(molecular_system):
            return form_XYZ
        else:
            raise NotImplementedError()

    if type(molecular_system)==dict:

        from molsysmt.forms.classes.api_dict_molecular_mechanics import this_dict_is_MolecularMechanicsDict
        from molsysmt.forms.classes.api_dict_molecular_mechanics import form_name as form_MolecularMechanicsDict
        from molsysmt.forms.classes.api_dict_simulation import this_dict_is_SimulationDict
        from molsysmt.forms.classes.api_dict_simulation import form_name as form_SimulationDict

        if this_dict_is_MolecularMechanicsDict(molecular_system):
            return form_MolecularMechanicsDict
        elif this_dict_is_SimulationDict(molecular_system):
            return form_SimulationDict
        else:
            raise NotImplementedError()

    if type(molecular_system)==str:

        if ':' in molecular_system:
            prefix=molecular_system.split(':')[0]
            if prefix+':id' in dict_is_form.keys():
                molecular_system=dict_is_form[prefix+':id']
            elif prefix+':seq' in dict_is_form.keys():
                molecular_system=dict_is_form[prefix+':seq']
        else:
            molecular_system=molecular_system.split('.')[-1]

    if is_list_or_tuple(molecular_system):
        output = [get_form(ii) for ii in molecular_system]
        return output

    try:
        return dict_is_form[type(molecular_system)]
    except:
        try:
            return dict_is_form[molecular_system]
        except:
            raise NotImplementedError()

