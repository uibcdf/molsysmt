form_name = 'string:pdb_id'
form_type = 'string'
form_info = ["", ""]

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
    'string:pdb_id': 'to_string_pdb_id',
    'file:pdb': 'to_file_pdb',
    'file:mmtf': 'to_file_mmtf',
    'file:msmpk': 'to_file_msmpk',
    'file:h5msm': 'to_file_h5msm',
    'file:fasta': 'to_file_fasta',
    'file:bcif': 'to_file_bcif',
    'file:bcif.gz': 'to_file_bcif_gz',
    'file:cif': 'to_file_cif',
    'file:cif.gz': 'to_file_cif_gz',
    'mmtf.MMTFDecoder': 'to_mmtf_MMTFDecoder',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
    'mdtraj.Topology': 'to_mdtraj_Topology',
    'mmcif.PdbxContainers.DataContainer': 'to_mmcif_PdbxContainers_DataContainer',
    'pdbfixer.PDBFixer': 'to_pdbfixer_PDBFixer',
    'openmm.Modeller': 'to_openmm_Modeller',
    'openmm.Topology': 'to_openmm_Topology',
    'openmm.PDBFile': 'to_openmm_PDBFile',
    'string:pdb_text': 'to_string_pdb_text',
    'nglview.NGLWidget': 'to_nglview_NGLWidget',
    }
