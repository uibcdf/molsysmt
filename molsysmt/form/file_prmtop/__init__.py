form_name = 'file:prmtop'
form_type = 'file'
form_info = ["AMBER parameter/topology file format",
             "https://ambermd.org/FileFormats.php#topology"]

from .is_file_prmtop import is_file_prmtop

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile, _to_openmm_AmberPrmtopFile
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology

_convert_to={
        'file:pdb': _to_file_pdb,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'openmm.AmberPrmtopFile': _to_openmm_AmberPrmtopFile,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.Topology': _to_openmm_Topology,
        }
