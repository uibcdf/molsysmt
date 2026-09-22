form_name = "file:pir"
form_type = "file"
form_info = ["PIR/NBRF sequence file format", "https://en.wikipedia.org/wiki/NBRF-PIR"]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402

from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402

from .extract import extract  # noqa: E402
from .copy import copy  # noqa: E402
from .add import add  # noqa: E402
from .merge import merge  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on


_convert_to = {
    "file:pir": "to_file_pir",
    "biopython.SeqRecord": "to_biopython_SeqRecord",
    "biopython.Seq": "to_biopython_Seq",
    "string:amino_acids_1": "to_string_amino_acids_1",
    "file:fasta": "to_file_fasta",
}
