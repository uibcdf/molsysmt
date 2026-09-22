form_name = "string:alphafold_id"
form_type = "string"
form_info = ["", ""]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

# Form metadata and export initialization must retain their established order.
# The wildcard imports expose the form's getter and setter functions.
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
    "string:alphafold_id": "to_string_alphafold_id",
    "file:pdb": "to_file_pdb",
    "file:h5msm": "to_file_h5msm",
    "file:fasta": "to_file_fasta",
    "file:bcif": "to_file_bcif",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "mmcif.PdbxContainers.DataContainer": "to_mmcif_PdbxContainers_DataContainer",
    "openmm.Modeller": "to_openmm_Modeller",
    "openmm.Topology": "to_openmm_Topology",
    "openmm.PDBFile": "to_openmm_PDBFile",
    "string:pdb_text": "to_string_pdb_text",
    "string:amino_acids_1": "to_string_amino_acids_1",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
}
