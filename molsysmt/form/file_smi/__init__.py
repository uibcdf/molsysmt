form_name = 'file:smi'
form_type = 'file'
form_info = ["SMILES file format (.smi)",
             "https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system"]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator


_convert_to = {
    'file:smi': 'to_file_smi',
    'string:smiles': 'to_string_smiles',
    'rdkit.Mol': 'to_rdkit_Mol',
    'molsysmt.Topology': 'to_molsysmt_Topology',
}
