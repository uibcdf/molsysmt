form_name = 'string:pdb_text'
form_type = 'string'
form_info = ["Protein Data Bank file format",
             "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

from .is_string_pdb_text import is_string_pdb_text

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_openmm_Simulation import to_openmm_Simulation, _to_openmm_Simulation
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_openmm_System import to_openmm_System, _to_openmm_System
from .to_openmm_PDBFile import to_openmm_PDBFile, _to_openmm_PDBFile
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer, _to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget

_convert_to={
        'file:pdb': _to_file_pdb,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'openmm.Simulation': _to_openmm_Simulation,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.Topology': _to_openmm_Topology,
        'openmm.System': _to_openmm_System,
        'openmm.PDBFile': _to_openmm_PDBFile,
        'pdbfixer.PDBFixer': _to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        }
