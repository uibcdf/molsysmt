form_name = 'file:mol2'
form_type = 'file'
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
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller
from .to_parmed_Structure import to_parmed_Structure
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'file:mol2': extract,
        'file:pdb': to_file_pdb,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'mdtraj.Topology': to_mdtraj_Topology,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'openmm.Topology': to_openmm_Topology,
        'openmm.Modeller': to_openmm_Modeller,
        'parmed.Structure': to_parmed_Structure,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
