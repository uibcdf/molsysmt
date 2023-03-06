form_name = 'mdtraj.Trajectory'
form_type = 'class'
form_info = ["", ""]

from .is_mdtraj_Trajectory import is_mdtraj_Trajectory

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_file_xtc import to_file_xtc, _to_file_xtc
from .to_biopython_Seq import to_biopython_Seq, _to_biopython_Seq
from .to_biopython_SeqRecord import to_biopython_SeqRecord, _to_biopython_SeqRecord
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer, _to_pdbfixer_PDBFixer
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_parmed_Structure import to_parmed_Structure, _to_parmed_Structure
from .to_pytraj_Trajectory import to_pytraj_Trajectory, _to_pytraj_Trajectory
from .to_pytraj_Topology import to_pytraj_Topology, _to_pytraj_Topology
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3

_dict_convert={
        'file:pdb': _to_file_pdb,
        'file:xtc': _to_file_xtc,
        'biopython.Seq': _to_biopython_Seq,
        'biopython.SeqRecord': _to_biopython_SeqRecord,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'openmm.Topology': _to_openmm_Topology,
        'openmm.Modeller': _to_openmm_Modeller,
        'pdbfixer.PDBFixer': _to_pdbfixer_PDBFixer,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'parmed.Structure': _to_parmed_Structure,
        'pytraj.Trajectory': _to_pytraj_Trajectory,
        'pytraj.Topology': _to_pytraj_Topology,
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids3,
        }
