form_name = 'molsysmt.MolSys'
form_type = 'class'
form_info = ["", ""]

from .is_molsysmt_MolSys import is_molsysmt_MolSys

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics, _to_molsysmt_MolecularMechanics
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_openmm_Context import to_openmm_Context, _to_openmm_Context
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_Simulation import to_openmm_Simulation, _to_openmm_Simulation
from .to_openmm_System import to_openmm_System, _to_openmm_System
from .to_pytraj_Topology import to_pytraj_Topology, _to_pytraj_Topology
from .to_pytraj_Trajectory import to_pytraj_Trajectory, _to_pytraj_Trajectory
from .to_biopython_Seq import to_biopython_Seq, _to_biopython_Seq
from .to_biopython_SeqRecord import to_biopython_SeqRecord, _to_biopython_SeqRecord
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer, _to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget
from .to_XYZ import to_XYZ, _to_XYZ
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3
from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text
from .to_file_msmpk import to_file_msmpk, _to_file_msmpk
from .to_file_pdb import to_file_pdb, _to_file_pdb

_dict_convert={
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'molsysmt.MolecularMechanics': _to_molsysmt_MolecularMechanics,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'openmm.Context': _to_openmm_Context,
        'openmm.Topology': _to_openmm_Topology,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.System': _to_openmm_System,
        'pytraj.Topology': _to_pytraj_Topology,
        'pytraj.Trajectory': _to_pytraj_Trajectory,
        'biopython.Seq': _to_biopython_Seq,
        'biopython.SeqRecord': _to_biopython_SeqRecord,
        'pdbfixer.PDBFixer': _to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        'XYZ': _to_XYZ,
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids3,
        'string:pdb_text': _to_string_pdb_text,
        'file:msmpk': _to_file_msmpk,
        'file:pdb': _to_file_pdb,
        }
