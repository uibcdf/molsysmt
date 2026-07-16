from .to_openmm_Modeller import to_openmm_Modeller
from .to_file_fasta import to_file_fasta
from .to_file_cif import to_file_cif
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_string_pdb_text import to_string_pdb_text
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_file_pdb import to_file_pdb
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_file_bcif_gz import to_file_bcif_gz
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_file_bcif import to_file_bcif
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
from .to_file_cif_gz import to_file_cif_gz
from .to_file_h5msm import to_file_h5msm
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_openmm_Topology import to_openmm_Topology
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_string_pdb_id import to_string_pdb_id
from .to_openmm_PDBFile import to_openmm_PDBFile
form_name = 'string:pdb_id'
form_type = 'string'
form_info = ["", ""]


def _extract_pdb_id(item):
    """Return the bare 4-character PDB ID from any accepted input variant.

    The canonical form is the plain 4-character code (e.g. '181L') or
    'pdb_id:181L'. The 'pdb:' prefix is accepted as a user-friendliness
    fallback only — it is NOT an official MolSysMT syntax and must NOT be
    documented or promoted as such.
    """
    lowered = item.lower()
    for prefix in ('pdb_id:', 'pdb:', 'pdb_'):
        if lowered.startswith(prefix):
            return lowered[len(prefix):]
    return lowered

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = True

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
    'string:pdb_id': to_string_pdb_id,
    'file:pdb': to_file_pdb,
    'file:h5msm': to_file_h5msm,
    'file:fasta': to_file_fasta,
    'file:bcif': to_file_bcif,
    'file:bcif.gz': to_file_bcif_gz,
    'file:cif': to_file_cif,
    'file:cif.gz': to_file_cif_gz,
    'molsysmt.MolSys': to_molsysmt_MolSys,
    'molsysmt.Topology': to_molsysmt_Topology,
    'molsysmt.Structures': to_molsysmt_Structures,
    'mdtraj.Trajectory': to_mdtraj_Trajectory,
    'mdtraj.Topology': to_mdtraj_Topology,
    'mmcif.PdbxContainers.DataContainer': to_mmcif_PdbxContainers_DataContainer,
    'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
    'openmm.Modeller': to_openmm_Modeller,
    'openmm.Topology': to_openmm_Topology,
    'openmm.PDBFile': to_openmm_PDBFile,
    'string:pdb_text': to_string_pdb_text,
    'nglview.NGLWidget': to_nglview_NGLWidget,
    }
