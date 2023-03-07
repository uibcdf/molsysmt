form_name = 'file:gro'
form_type = 'file'
form_info = ["Gromacs gro file format",
             "http://manual.gromacs.org/documentation/2018/user-guide/file-formats.html#gro"]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_mdtraj_GroTrajectoryFile import to_mdtraj_GroTrajectoryFile, _to_mdtraj_GroTrajectoryFile
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_GromacsGroFile import to_openmm_GromacsGroFile, _to_openmm_GromacsGroFile
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget

_convert_to={
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'mdtraj.GroTrajectoryFile': _to_mdtraj_GroTrajectoryFile,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'openmm.Topology': _to_openmm_Topology,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.GromacsGroFile': _to_openmm_GromacsGroFile,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        }
