form_name = 'file:mol2'
form_type = 'file'
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
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_pdb import to_file_pdb
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller
from .to_parmed_Structure import to_parmed_Structure
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'file:mol2': extract,
        'file:pdb': to_file_pdb,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'mdtraj.Topology': to_mdtraj_Topology,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'openmm.Topology': to_openmm_Topology,
        'openmm.Modeller': to_openmm_Modeller,
        'parmed.Structure': to_parmed_Structure,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
