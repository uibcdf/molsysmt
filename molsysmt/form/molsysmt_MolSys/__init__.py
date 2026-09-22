from .add_bonds import add_bonds
from .remove_bonds import remove_bonds

form_name = "molsysmt.MolSys"
form_type = "class"
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
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
from .get_mechanical_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402

# These names were historically exposed through the wildcard import from .set.
import numpy as np  # noqa: E402
from molsysmt._private.smonitor import ArgumentError  # noqa: E402
# isort: on

_convert_to = {
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolecularMechanics": "to_molsysmt_MolecularMechanics",
    "molsysmt.MolecularMechanicsDict": "to_molsysmt_MolecularMechanicsDict",
    "molsysmt.MolSysBuilder": "to_molsysmt_MolSysBuilder",
    "molsysmt.MolSysDict": "to_molsysmt_MolSysDict",
    "networkx.Graph": "to_networkx_Graph",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
    "molsysviewer.MolSysView": "to_molsysviewer_MolSysView",
    "openmm.Context": "to_openmm_Context",
    "openmm.Topology": "to_openmm_Topology",
    "openmm.Modeller": "to_openmm_Modeller",
    "openmm.System": "to_openmm_System",
    "openmm.Simulation": "to_openmm_Simulation",
    "parmed.Structure": "to_parmed_Structure",
    "pdbfixer.PDBFixer": "to_pdbfixer_PDBFixer",
    "pytraj.Topology": "to_pytraj_Topology",
    "pytraj.Trajectory": "to_pytraj_Trajectory",
    "biopython.Seq": "to_biopython_Seq",
    "biopython.SeqRecord": "to_biopython_SeqRecord",
    "biopython.PDBStructure": "to_biopython_PDBStructure",
    "molsysmt.ViewerJSON": "to_molsysmt_ViewerJSON",
    "rdkit.Mol": "to_rdkit_Mol",
    "XYZ": "to_XYZ",
    "string:pdb_text": "to_string_pdb_text",
    "string:amino_acids_1": "to_string_amino_acids_1",
    "string:amino_acids_3": "to_string_amino_acids_3",
    "file:h5msm": "to_file_h5msm",
    "file:molsys_yaml": "to_file_molsys_yaml",
    "file:pdb": "to_file_pdb",
    "file:psf": "to_file_psf",
}

_conversion_opt_kwargs = {
    "string:pdb_text": ["pdb_chain_id"],
    "pdbfixer.PDBFixer": ["pdb_chain_id"],
    "openmm.Simulation": ["collisions_rate", "integration_timestep"],
}
