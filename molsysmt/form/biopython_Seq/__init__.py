form_name = 'biopython.Seq'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .copy import copy
from .add import add
from .get import *
from .set import *
from .iterators import TopologyIterator

from .to_biopython_SeqRecord import to_biopython_SeqRecord

_convert_to={
        'biopython.SeqRecord': to_biopython_SeqRecord,
        }
