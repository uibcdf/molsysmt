form_name = 'parmed.Structure'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_mol2 import to_file_mol2
from .to_file_pdb import to_file_pdb
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'file:mol2': to_file_mol2,
        'file:pdb': to_file_pdb,
        'mdtraj.Topology': to_mdtraj_Topology,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'openmm.Modeller': to_openmm_Modeller,
        'openmm.Topology': to_openmm_Topology,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        }
