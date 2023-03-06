form_name = 'molsysmt.Topology'
form_type = 'class'
form_info = ["", ""]

from .is_molsysmt_Topology import is_molsysmt_Topology

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text
from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_pytraj_Topology import to_pytraj_Topology, _to_pytraj_Topology
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys

_dict_convert={
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids3,
        'string:pdb_text': _to_string_pdb_text,
        'file:pdb': _to_file_pdb,
        'openmm.Topology': _to_openmm_Topology,
        'pytraj.Topology': _to_pytraj_Topology,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        }
