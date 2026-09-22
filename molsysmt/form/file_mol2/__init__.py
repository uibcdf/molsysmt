form_name = "file:mol2"
form_type = "file"
form_info = ["", ""]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"

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
from .get_mechanical_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on


_convert_to = {
    "file:mol2": "to_file_mol2",
    "file:pdb": "to_file_pdb",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "openmm.Topology": "to_openmm_Topology",
    "openmm.Modeller": "to_openmm_Modeller",
    "parmed.Structure": "to_parmed_Structure",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
}


piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = False
