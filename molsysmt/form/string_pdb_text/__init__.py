form_name = 'string:pdb_text'
form_type = 'string'
form_info = ["Protein Data Bank file format",
             "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

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
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_openmm_Simulation import to_openmm_Simulation
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_System import to_openmm_System
from .to_openmm_PDBFile import to_openmm_PDBFile
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'string:pdb_text': extract,
        'file:pdb': to_file_pdb,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'mdtraj.Topology': to_mdtraj_Topology,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'openmm.Simulation': to_openmm_Simulation,
        'openmm.Modeller': to_openmm_Modeller,
        'openmm.Topology': to_openmm_Topology,
        'openmm.System': to_openmm_System,
        'openmm.PDBFile': to_openmm_PDBFile,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
