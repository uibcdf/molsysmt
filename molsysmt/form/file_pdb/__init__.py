# Form metadata and export initialization retain their established import order.
# isort: off
form_name = "file:pdb"
form_type = "file"
form_info = [
    "Protein Data Bank file format",
    "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html",
]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

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

from .download import download  # noqa: E402
from .replace_HETATM_by_ATOM_in_terminal_cappings import (  # noqa: E402
    replace_HETATM_by_ATOM_in_terminal_cappings,
)
from .has_atoms_with_alternate_locations import has_atoms_with_alternate_locations  # noqa: E402
# isort: on


_convert_to = {
    "file:pdb": "to_file_pdb",
    "string:pdb_text": "to_string_pdb_text",
    "file:mol2": "to_file_mol2",
    "MDAnalysis.topology.PDBParser": "to_MDAnalysis_topology_PDBParser",
    "MDAnalysis.Topology": "to_MDAnalysis_Topology",
    "MDAnalysis.Universe": "to_MDAnalysis_Universe",
    "mdtraj.PDBTrajectoryFile": "to_mdtraj_PDBTrajectoryFile",
    "mdtraj.Topology": "to_mdtraj_Topology",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.PDBFileHandler": "to_molsysmt_PDBFileHandler",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
    "openmm.Modeller": "to_openmm_Modeller",
    "openmm.PDBFile": "to_openmm_PDBFile",
    "openmm.Simulation": "to_openmm_Simulation",
    "openmm.System": "to_openmm_System",
    "openmm.Topology": "to_openmm_Topology",
    "parmed.Structure": "to_parmed_Structure",
    "pdbfixer.PDBFixer": "to_pdbfixer_PDBFixer",
    "pytraj.Topology": "to_pytraj_Topology",
    "pytraj.Trajectory": "to_pytraj_Trajectory",
}

_conversion_opt_kwargs = {
    "pytraj.Topology": ["max_bond_length"],
    "openmm.Simulation": ["collisions_rate", "integration_timestep"],
}
