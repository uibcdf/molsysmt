from .is_file_pdb import is_file_pdb

form_name = 'file:pdb'
form_type = 'file'
form_info = ["Protein Data Bank file format", "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .download import download
from .replace_HETATM_by_ATOM_in_terminal_cappings import replace_HETATM_by_ATOM_in_terminal_cappings
from .has_atoms_with_alternate_locations import has_atoms_with_alternate_locations

from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text
from .to_file_mol2 import to_file_mol2, _to_file_mol2
from .to_MDAnalysis_topology_PDBParser import to_MDAnalysis_topology_PDBParser, _to_MDAnalysis_topology_PDBParser
from .to_MDAnalysis_Topology import to_MDAnalysis_Topology, _to_MDAnalysis_Topology
from .to_MDAnalysis_Universe import to_MDAnalysis_Universe, _to_MDAnalysis_Universe
from .to_mdtraj_PDBTrajectoryFile import to_mdtraj_PDBTrajectoryFile, _to_mdtraj_PDBTrajectoryFile
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_PDBFile import to_openmm_PDBFile, _to_openmm_PDBFile
from .to_openmm_Simulation import to_openmm_Simulation, _to_openmm_Simulation
from .to_openmm_System import to_openmm_System, _to_openmm_System
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_parmed_Structure import to_parmed_Structure, _to_parmed_Structure
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer, _to_pdbfixer_PDBFixer
from .to_pytraj_Topology import to_pytraj_Topology, _to_pytraj_Topology
from .to_pytraj_Trajectory import to_pytraj_Trajectory, _to_pytraj_Trajectory
