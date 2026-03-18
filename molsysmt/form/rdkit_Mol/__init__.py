form_name = 'rdkit.Mol'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

from .to_string_smiles import to_string_smiles
from .to_file_smi import to_file_smi

_convert_to = {
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'string:smiles': to_string_smiles,
    'file:smi': to_file_smi,
}

from .is_form import is_form
from .attributes import attributes
from .get_topological_attributes import *
from .get_structural_attributes import *
from .has_attribute import has_attribute
