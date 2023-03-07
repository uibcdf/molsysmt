form_name = 'parmed.Structure'
form_type = 'class'
form_info = ["", ""]

from .is_parmed_Structure import is_parmed_Structure

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_mol2 import to_file_mol2, _to_file_mol2
from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures

_convert_to={
        'file:mol2': _to_file_mol2,
        'file:pdb': _to_file_pdb,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.Topology': _to_openmm_Topology,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        }
