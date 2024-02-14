form_name = 'molsysmt.MolSysOld'
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
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_openmm_Context import to_openmm_Context
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_Simulation import to_openmm_Simulation
from .to_openmm_System import to_openmm_System
from .to_parmed_Structure import to_parmed_Structure
from .to_pytraj_Topology import to_pytraj_Topology
from .to_pytraj_Trajectory import to_pytraj_Trajectory
from .to_biopython_Seq import to_biopython_Seq
from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_XYZ import to_XYZ
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3
from .to_string_pdb_text import to_string_pdb_text
from .to_file_msmpk import to_file_msmpk
from .to_file_pdb import to_file_pdb
from .to_file_psf import to_file_psf

_convert_to={
        'molsysmt.MolSysOld': extract,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'molsysmt.MolecularMechanicsDict': to_molsysmt_MolecularMechanicsDict,
        'mdtraj.Topology': to_mdtraj_Topology,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'openmm.Context': to_openmm_Context,
        'openmm.Topology': to_openmm_Topology,
        'openmm.Modeller': to_openmm_Modeller,
        'openmm.System': to_openmm_System,
        'parmed.Structure': to_parmed_Structure,
        'pytraj.Topology': to_pytraj_Topology,
        'pytraj.Trajectory': to_pytraj_Trajectory,
        'biopython.Seq': to_biopython_Seq,
        'biopython.SeqRecord': to_biopython_SeqRecord,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'XYZ': to_XYZ,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids3,
        'string:pdb_text': to_string_pdb_text,
        'file:msmpk': to_file_msmpk,
        'file:pdb': to_file_pdb,
        'file:psf': to_file_psf,
        }

