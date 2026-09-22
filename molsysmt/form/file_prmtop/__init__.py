form_name = "file:prmtop"
form_type = "file"
form_info = [
    "AMBER parameter/topology file format",
    "https://ambermd.org/FileFormats.php#topology",
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
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on


_convert_to = {
    "file:prmtop": "to_file_prmtop",
    "file:pdb": "to_file_pdb",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
    "openmm.AmberPrmtopFile": "to_openmm_AmberPrmtopFile",
    "openmm.Modeller": "to_openmm_Modeller",
    "openmm.Topology": "to_openmm_Topology",
}
