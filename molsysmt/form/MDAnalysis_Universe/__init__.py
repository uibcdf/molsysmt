form_name = 'MDAnalysis.Universe'
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
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_file_pdb import to_file_pdb
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld

_convert_to={
        'MDAnalysis.Universe': extract,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'file:pdb': to_file_pdb,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        }
