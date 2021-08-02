from molsysmt import puw
from molsysmt.forms import dict_is_form
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import digest_output
from molsysmt.tools.items import item_is_file, item_is_string
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

        from molsysmt.forms.classes.api_molsysmt_MolecularMechanicsDict import this_dict_is_MolecularMechanicsDict
        from molsysmt.forms.classes.api_molsysmt_MolecularMechanicsDict import form_name as form_MolecularMechanicsDict
        from molsysmt.forms.classes.api_molsysmt_SimulationDict import this_dict_is_SimulationDict
        from molsysmt.forms.classes.api_molsysmt_SimulationDict import form_name as form_SimulationDict
        from molsysmt.forms.classes.api_molsysmt_TrajectoryDict import this_dict_is_TrajectoryDict
        from molsysmt.forms.classes.api_molsysmt_TrajectoryDict import form_name as form_TrajectoryDict

        if this_dict_is_MolecularMechanicsDict(molecular_system):
            return form_MolecularMechanicsDict
        elif this_dict_is_SimulationDict(molecular_system):
            return form_SimulationDict
        elif this_dict_is_TrajectoryDict(molecular_system):
            return form_TrajectoryDict
        else:
            raise NotImplementedError()

    if type(molecular_system)==str:
        file_form = item_is_file(molecular_system)
        if file_form:
            return dict_is_form[file_form]
        string_form = item_is_string(molecular_system)
        if string_form:
            return dict_is_form[string_form]

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

