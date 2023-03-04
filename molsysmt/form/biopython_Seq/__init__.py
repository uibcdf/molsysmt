form_name = 'biopython.Seq'
form_type = 'class'
form_info = ["", ""]

from .is_biopython_Seq import is_biopython_Seq

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_biopython_SeqRecord import to_biopython_SeqRecord, _to_biopython_SeqRecord

_dict_convert={
        'biopython.SeqRecord': _to_biopython_SeqRecord,
        }
