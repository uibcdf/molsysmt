form_name = 'openmm.PDBFile'
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

from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_openmm_Topology import to_openmm_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'openmm.PDBFile': extract,
        'mdtraj.Topology': to_mdtraj_Topology,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Structures': to_molsysmt_Structures,
        'openmm.Topology': to_openmm_Topology,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'molsysmt.Topology': to_molsysmt_Topology,
        'nglview.NGLWidget': to_nglview_NGLWidget
        }
