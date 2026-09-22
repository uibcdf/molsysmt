form_name = "mmcif.PdbxContainers.DataContainer"
form_type = "class"
form_info = ["", ""]

# https://mmcif.wwpdb.org/
# https://github.com/rcsb/py-mmcif

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = False
bonds_can_be_computed = False

_convert_to = {
    "mmcif.PdbxContainers.DataContainer": "to_mmcif_PdbxContainers_DataContainer",
    "file:pdb": "to_file_pdb",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolecularMechanics": "to_molsysmt_MolecularMechanics",
    "openmm.Topology": "to_openmm_Topology",
    "string:amino_acids_1": "to_string_amino_acids_1",
    "string:amino_acids_3": "to_string_amino_acids_3",
    "string:pdb_text": "to_string_pdb_text",
    "string:pdb_id": "to_string_pdb_id",
}

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
