from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_biopython_Seq import to_biopython_Seq
form_name = 'biopython.Seq'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

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
from .iterators import TopologyIterator


_convert_to={
        'biopython.Seq': to_biopython_Seq,
        'biopython.SeqRecord': to_biopython_SeqRecord,
        }


piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False
