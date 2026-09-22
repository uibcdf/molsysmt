# Form metadata and export initialization retain their established import order.
# isort: off
from .to_file_h5msm import dump_topology_to_h5msm

form_name = "molsysmt.Topology"
form_type = "class"
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = False

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

from .add_bonds import add_bonds  # noqa: E402
from .remove_bonds import remove_bonds  # noqa: E402
# isort: on

_convert_to = {
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.TopologyDict": "to_molsysmt_TopologyDict",
    "file:topology_yaml": "to_file_topology_yaml",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "molsysmt.ViewerJSON": "to_molsysmt_ViewerJSON",
    "string:amino_acids_1": "to_string_amino_acids_1",
    "string:amino_acids_3": "to_string_amino_acids_3",
    "string:pdb_text": "to_string_pdb_text",
    "file:h5msm": "to_file_h5msm",
    "file:pdb": "to_file_pdb",
    "file:psf": "to_file_psf",
    "networkx.Graph": "to_networkx_Graph",
    "openmm.Topology": "to_openmm_Topology",
    "parmed.Structure": "to_parmed_Structure",
    "pytraj.Topology": "to_pytraj_Topology",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
}
