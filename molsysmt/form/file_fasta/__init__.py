form_name = 'file:fasta'
form_type = 'file'
form_info = ["FASTA sequence file format", "https://en.wikipedia.org/wiki/FASTA_format"]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

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
    'file:fasta': 'to_file_fasta',
    'biopython.SeqRecord': 'to_biopython_SeqRecord',
    'biopython.Seq': 'to_biopython_Seq',
    'string:amino_acids_1': 'to_string_amino_acids_1',
    'molsysmt.Topology': 'to_molsysmt_Topology',
}
