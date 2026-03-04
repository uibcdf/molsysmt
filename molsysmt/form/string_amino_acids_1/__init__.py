from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_biopython_Seq import to_biopython_Seq
from .to_string_amino_acids_3 import to_string_amino_acids_3
from .to_string_amino_acids_1 import to_string_amino_acids_1
form_name = 'string:amino_acids_1'
form_type = 'string'
form_info = ["", ""]

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
from .append_structures import append_structures
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import TopologyIterator


_convert_to={
        'string:amino_acids_1': to_string_amino_acids_1,
        'string:amino_acids_3': to_string_amino_acids_3,
        'biopython.SeqRecord': to_biopython_SeqRecord,
        'biopython.Seq': to_biopython_Seq,
        }
