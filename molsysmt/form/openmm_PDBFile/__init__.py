form_name = 'openmm.PDBFile'
form_type = 'class'
form_info = ["", ""]

from .is_openmm_PDBFile import is_openmm_PDBFile

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget

_dict_convert={
        'mdtraj.Topology': _to_mdtraj_Topology,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'openmm.Topology': _to_openmm_Topology,
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'nglview.NGLWidget': _to_nglview_NGLWidget
        }
