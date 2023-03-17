form_name = 'mdtraj.Trajectory'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_pdb import to_file_pdb
from .to_file_xtc import to_file_xtc
from .to_biopython_Seq import to_biopython_Seq
from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_parmed_Structure import to_parmed_Structure
from .to_pytraj_Trajectory import to_pytraj_Trajectory
from .to_pytraj_Topology import to_pytraj_Topology
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3

_convert_to={
        'mdtraj.Trajectory': extract,
        'file:pdb': to_file_pdb,
        'file:xtc': to_file_xtc,
        'biopython.Seq': to_biopython_Seq,
        'biopython.SeqRecord': to_biopython_SeqRecord,
        'mdtraj.Topology': to_mdtraj_Topology,
        'openmm.Topology': to_openmm_Topology,
        'openmm.Modeller': to_openmm_Modeller,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.Topology': to_molsysmt_Topology,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'parmed.Structure': to_parmed_Structure,
        'pytraj.Trajectory': to_pytraj_Trajectory,
        'pytraj.Topology': to_pytraj_Topology,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids3,
        }
