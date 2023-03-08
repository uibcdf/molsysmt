form_name = 'openmm.Topology'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text
from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_Simulation import to_openmm_Simulation, _to_openmm_Simulation
from .to_openmm_Context import to_openmm_Context, _to_openmm_Context
from .to_openmm_PDBFile import to_openmm_PDBFile, _to_openmm_PDBFile
from .to_openmm_System import to_openmm_System, _to_openmm_System
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer, _to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3

_convert_to={
        'string:pdb_text': _to_string_pdb_text,
        'file:pdb': _to_file_pdb,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.Simulation': _to_openmm_Simulation,
        'openmm.Context': _to_openmm_Context,
        'openmm.PDBFile': _to_openmm_PDBFile,
        'openmm.System': _to_openmm_PDBFile,
        'pdbfixer.PDBFixer': _to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids3,
        }
