form_name = 'MDAnalysis.Universe'
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

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_file_pdb import to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'MDAnalysis.Universe': extract,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'file:pdb': to_file_pdb,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        }
