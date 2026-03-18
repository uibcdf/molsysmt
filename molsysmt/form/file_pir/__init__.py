from .to_file_pir import to_file_pir
from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_biopython_Seq import to_biopython_Seq
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_file_fasta import to_file_fasta

form_name = 'file:pir'
form_type = 'file'
form_info = ["PIR/NBRF sequence file format", "https://en.wikipedia.org/wiki/NBRF-PIR"]

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
    'file:pir': to_file_pir,
    'biopython.SeqRecord': to_biopython_SeqRecord,
    'biopython.Seq': to_biopython_Seq,
    'string:amino_acids_1': to_string_amino_acids_1,
    'file:fasta': to_file_fasta,
}
