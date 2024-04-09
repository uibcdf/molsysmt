form_name = 'openmm.Topology'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import TopologyIterator

from .write_topology_in_h5msm import write_topology_in_h5msm

from .to_string_pdb_text import to_string_pdb_text
from .to_file_pdb import to_file_pdb
from .to_file_psf import to_file_psf
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_networkx_Graph import to_networkx_Graph
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_Simulation import to_openmm_Simulation
from .to_openmm_Context import to_openmm_Context
from .to_openmm_PDBFile import to_openmm_PDBFile
from .to_openmm_System import to_openmm_System
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3
from .to_parmed_Structure import to_parmed_Structure

_convert_to={
        'openmm.Topology': extract,
        'string:pdb_text': to_string_pdb_text,
        'file:pdb': to_file_pdb,
        'file:psf': to_file_psf,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'mdtraj.Topology': to_mdtraj_Topology,
        'networkx.Graph': to_networkx_Graph,
        'openmm.Modeller': to_openmm_Modeller,
        'openmm.Simulation': to_openmm_Simulation,
        'openmm.Context': to_openmm_Context,
        'openmm.PDBFile': to_openmm_PDBFile,
        'openmm.System': to_openmm_PDBFile,
        'parmed.Structure': to_parmed_Structure,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids3,
        }
