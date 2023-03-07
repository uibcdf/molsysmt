form_name = 'string:pdb_id'
form_type = 'string'
form_info = ["", ""]

from .is_string_pdb_id import is_string_pdb_id

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_file_mmtf import to_file_mmtf, _to_file_mmtf
from .to_file_msmpk import to_file_msmpk, _to_file_msmpk
from .to_file_fasta import to_file_fasta, _to_file_fasta
from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder, _to_mmtf_MMTFDecoder
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer, _to_pdbfixer_PDBFixer
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_openmm_PDBFile import to_openmm_PDBFile, _to_openmm_PDBFile
from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text
from .to_nglview_NGLWidget import to_nglview_NGLWidget, _to_nglview_NGLWidget

_convert_to={
        'file:pdb': _to_file_pdb,
        'file:mmtf': _to_file_mmtf,
        'file:msmpk': _to_file_msmpk,
        'file:fasta': _to_file_fasta,
        'mmtf.MMTFDecoder': _to_mmtf_MMTFDecoder,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'mdtraj.Topology': _to_mdtraj_Topology,
        'pdbfixer.PDBFixer': _to_pdbfixer_PDBFixer,
        'openmm.Modeller': _to_openmm_Modeller,
        'openmm.Topology': _to_openmm_Topology,
        'openmm.PDBFile': _to_openmm_PDBFile,
        'string:pdb_text': _to_string_pdb_text,
        'nglview.NGLWidget': _to_nglview_NGLWidget,
        }
