form_name = "string:uniprot_id"
form_type = "string"
form_info = ["UniProt accession number string", "https://www.uniprot.org/"]

piped_topological_attribute = "molsysmt.Topology"
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
from .append_structures import append_structures  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import TopologyIterator  # noqa: E402
# isort: on


_convert_to = {
    "string:uniprot_id": "to_string_uniprot_id",
    "file:fasta": "to_file_fasta",
    "molsysmt.Topology": "to_molsysmt_Topology",
}
