form_name = 'molsysmt.Topology'
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
from .iterators import TopologyIterator

from .to_string_aminoacids3 import to_string_aminoacids3
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_pdb_text import to_string_pdb_text
from .to_file_pdb import to_file_pdb
from .to_file_psf import to_file_psf
from .to_openmm_Topology import to_openmm_Topology
from .to_parmed_Structure import to_parmed_Structure
from .to_pytraj_Topology import to_pytraj_Topology
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_molsysmt_MolSys import to_molsysmt_MolSys

_convert_to={
        'molsysmt.Topology': extract,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids3,
        'string:pdb_text': to_string_pdb_text,
        'file:pdb': to_file_pdb,
        'file:psf': to_file_psf,
        'openmm.Topology': to_openmm_Topology,
        'parmed.Structure': to_parmed_Structure,
        'pytraj.Topology': to_pytraj_Topology,
        'mdtraj.Topology': to_mdtraj_Topology,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        }
