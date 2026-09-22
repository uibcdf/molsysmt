form_name = "file:top"
form_type = "file"
form_info = [
    "GROMACS topology file format",
    "https://manual.gromacs.org/current/reference-manual/file-formats.html#top",
]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
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
    "file:top": "to_file_top",
    "parmed.GromacsTopologyFile": "to_parmed_GromacsTopologyFile",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
}
