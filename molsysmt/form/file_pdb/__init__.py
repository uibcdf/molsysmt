form_name = 'file:pdb'
form_type = 'file'
form_info = ["Protein Data Bank file format", "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = False
bonds_can_be_computed = True

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .download import download
from .replace_HETATM_by_ATOM_in_terminal_cappings import replace_HETATM_by_ATOM_in_terminal_cappings
from .has_atoms_with_alternate_locations import has_atoms_with_alternate_locations

from .to_string_pdb_text import to_string_pdb_text
from .to_file_mol2 import to_file_mol2
from .to_MDAnalysis_Topology import to_MDAnalysis_Topology
from .to_MDAnalysis_Universe import to_MDAnalysis_Universe
from .to_mdtraj_PDBTrajectoryFile import to_mdtraj_PDBTrajectoryFile
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_PDBFile import to_openmm_PDBFile
from .to_openmm_Simulation import to_openmm_Simulation
from .to_openmm_System import to_openmm_System
from .to_openmm_Topology import to_openmm_Topology
from .to_parmed_Structure import to_parmed_Structure
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_pytraj_Topology import to_pytraj_Topology
from .to_pytraj_Trajectory import to_pytraj_Trajectory

_convert_to={
        'file:pdb': extract,
        'string:pdb_text': to_string_pdb_text,
        'file:mol2': to_file_mol2,
        'MDAnalysis.Topology': to_MDAnalysis_Topology,
        'MDAnalysis.Universe': to_MDAnalysis_Universe,
        'mdtraj.PDBTrajectoryFile': to_mdtraj_PDBTrajectoryFile,
        'mdtraj.Topology': to_mdtraj_Topology,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.PDBFileHandler': to_molsysmt_PDBFileHandler,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'openmm.Modeller': to_openmm_Modeller,
        'openmm.PDBFile': to_openmm_PDBFile,
        'openmm.Simulation': to_openmm_Simulation,
        'openmm.System': to_openmm_System,
        'openmm.Topology': to_openmm_Topology,
        'parmed.Structure': to_parmed_Structure,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'pytraj.Topology': to_pytraj_Topology,
        'pytraj.Trajectory': to_pytraj_Trajectory,
        }

