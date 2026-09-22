form_name = "string:pdb_text"
form_type = "string"
form_info = [
    "Protein Data Bank file format",
    "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html",
]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = False
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
    "string:pdb_text": "to_string_pdb_text",
    "file:pdb": "to_file_pdb",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.PDBFileHandler": "to_molsysmt_PDBFileHandler",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "openmm.Simulation": "to_openmm_Simulation",
    "openmm.Modeller": "to_openmm_Modeller",
    "openmm.Topology": "to_openmm_Topology",
    "openmm.System": "to_openmm_System",
    "openmm.PDBFile": "to_openmm_PDBFile",
    "pdbfixer.PDBFixer": "to_pdbfixer_PDBFixer",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
}
