form_name = "file:gro"
form_type = "file"
form_info = [
    "Gromacs gro file format",
    "http://manual.gromacs.org/documentation/2018/user-guide/file-formats.html#gro",
]

piped_topological_attribute = "molsysmt.MolSys"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = False
bonds_can_be_computed = True

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
    "file:gro": extract,
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "mdtraj.GroTrajectoryFile": "to_mdtraj_GroTrajectoryFile",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.GROFileHandler": "to_molsysmt_GROFileHandler",
    "openmm.Topology": "to_openmm_Topology",
    "openmm.Modeller": "to_openmm_Modeller",
    "openmm.GromacsGroFile": "to_openmm_GromacsGroFile",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
}
