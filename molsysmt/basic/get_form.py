from molsysmt import puw
from molsysmt.forms import dict_is_form
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import digest_output
from molsysmt.forms import file_extensions_recognized
from molsysmt.forms import string_names_recognized
from molsysmt.native.molecular_system import MolecularSystem
from molsysmt._private_tools.exceptions import *

def get_form(molecular_system):

    if is_list_or_tuple(molecular_system):
        output = [get_form(ii) for ii in molecular_system]
        return output

    type_molecular_system = molecular_system.__class__.__module__+'.'+molecular_system.__class__.__name__

    if type_molecular_system in dict_is_form:

        return dict_is_form[type_molecular_system]

    if type_molecular_system=='molsysmt.native.molecular_system.MolecularSystem':

        _, output = molecular_system.get_items()
        output = digest_output(output)
        return output

    if type_molecular_system=='builtins.dict':

        from molsysmt.forms.api_molsysmt_MolecularMechanicsDict import this_dict_is_MolecularMechanicsDict
        from molsysmt.forms.api_molsysmt_MolecularMechanicsDict import form_name as form_MolecularMechanicsDict
        from molsysmt.forms.api_molsysmt_SimulationDict import this_dict_is_SimulationDict
        from molsysmt.forms.api_molsysmt_SimulationDict import form_name as form_SimulationDict
        from molsysmt.forms.api_molsysmt_TrajectoryDict import this_dict_is_TrajectoryDict
        from molsysmt.forms.api_molsysmt_TrajectoryDict import form_name as form_TrajectoryDict

        if this_dict_is_MolecularMechanicsDict(molecular_system):
            return form_MolecularMechanicsDict
        elif this_dict_is_SimulationDict(molecular_system):
            return form_SimulationDict
        elif this_dict_is_TrajectoryDict(molecular_system):
            return form_TrajectoryDict
        else:
            raise NotImplementedError()

    if type_molecular_system=='builtins.str':

        file_extension = molecular_system.split('.')[-1].lower()
        if file_extension in file_extensions_recognized:
            return 'file:'+file_extension

        if ':' in molecular_system:

            string_name = molecular_system.split(':')[0]
            if string_name in string_names_recognized:
                return 'string:'+string_name

        from molsysmt.tools.string_pdb_text import is_string_pdb_text
        from molsysmt.tools.string_pdb_id import is_string_pdb_id
        from molsysmt.tools.string_aminoacids3 import is_string_aminoacids3
        from molsysmt.tools.string_aminoacids1 import is_string_aminoacids1

        if is_string_pdb_id(molecular_system):
            return 'string:pdb_id'
        elif is_string_pdb_text(molecular_system):
            return 'string:pdb_text'
        elif is_string_aminoacids3(molecular_system):
            return 'string:aminoacids3'
        elif is_string_aminoacids1(molecular_system):
            return 'string:aminoacids1'
        else:
            raise NotImplementedError()

    if puw.is_quantity(molecular_system):

        from molsysmt.forms.api_XYZ import this_Quantity_is_XYZ
        from molsysmt.forms.api_XYZ import form_name as form_XYZ

        if this_Quantity_is_XYZ(molecular_system):
            return form_XYZ
        else:
            raise NotImplementedError()

    raise NotImplementedError()


