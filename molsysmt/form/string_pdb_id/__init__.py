form_name = 'string:pdb_id'
form_type = 'string'
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

from .to_file_pdb import to_file_pdb
from .to_file_mmtf import to_file_mmtf
from .to_file_msmpk import to_file_msmpk
from .to_file_fasta import to_file_fasta
from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_PDBFile import to_openmm_PDBFile
from .to_string_pdb_text import to_string_pdb_text
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'string:pdb_id': extract,
        'file:pdb': to_file_pdb,
        'file:mmtf': to_file_mmtf,
        'file:msmpk': to_file_msmpk,
        'file:fasta': to_file_fasta,
        'mmtf.MMTFDecoder': to_mmtf_MMTFDecoder,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'mdtraj.Topology': to_mdtraj_Topology,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        'openmm.Modeller': to_openmm_Modeller,
        'openmm.Topology': to_openmm_Topology,
        'openmm.PDBFile': to_openmm_PDBFile,
        'string:pdb_text': to_string_pdb_text,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
