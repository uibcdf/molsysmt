form_name = 'MDAnalysis.Universe'
form_type = 'class'
form_info = ["", ""]

from .is_MDAnalysis_Universe import is_MDAnalysis_Universe

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures

_convert_to={
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'file:pdb': _to_file_pdb,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        }
