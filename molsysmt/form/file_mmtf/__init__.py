from .download import download

form_name = 'file:mmtf'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = None
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
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from depdigest import is_installed

if is_installed('mdtraj'):
    

_convert_to={
        'file:mmtf': 'to_file_mmtf',
        'file:pdb': 'to_file_pdb',
        'mmtf.MMTFDecoder': 'to_mmtf_MMTFDecoder',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'openmm.Topology': 'to_openmm_Topology',
        'string:amino_acids_1': 'to_string_amino_acids_1',
        'string:amino_acids_3': 'to_string_amino_acids_3',
        'string:pdb_text': 'to_string_pdb_text',
        }
