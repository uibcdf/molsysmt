form_name = 'mdtraj.HDF5TrajectoryFile'
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
from .to_openmm_Topology import to_openmm_Topology
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys

_convert_to={
        'mdtraj.HDF5TrajectoryFile': extract,
        'mdtraj.Topology': to_mdtraj_Topology,
        'openmm.Topology': to_openmm_Topology,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        }
