form_name = "file:h5"
form_type = "file"
form_info = ["", ""]

piped_topological_attribute = "mdtraj.Topology"
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
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
    "file:h5": "to_file_h5",
    "mdtraj.HDF5TrajectoryFile": "to_mdtraj_HDF5TrajectoryFile",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
    "openmm.Topology": "to_openmm_Topology",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "file:pdb": "to_file_pdb",
    "file:h5msm": "to_file_h5msm",
}
