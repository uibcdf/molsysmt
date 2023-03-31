form_name = 'openmm.Modeller'
form_type = 'class'
form_info = ["", ""]

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

from .to_file_pdb import to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_openmm_System import to_openmm_System
from .to_openmm_Simulation import to_openmm_Simulation
from .to_openmm_Topology import to_openmm_Topology
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'openmm.Modeller': extract,
        'file:pdb': to_file_pdb,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'mdtraj.Topology': to_mdtraj_Topology,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'openmm.System': to_openmm_System,
        'openmm.Simulation': to_openmm_Simulation,
        'openmm.Topology': to_openmm_Topology,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
