form_name = 'string:alphafold_id'
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

from .to_file_bcif import to_file_bcif
from .to_file_pdb import to_file_pdb
from .to_file_fasta import to_file_fasta
from .to_file_h5msm import to_file_h5msm
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
from .to_openmm_Modeller import to_openmm_Modeller
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_PDBFile import to_openmm_PDBFile
from .to_string_pdb_text import to_string_pdb_text
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
    'string:alphafold_id': extract,
    'file:pdb': to_file_pdb,
    'file:h5msm': to_file_h5msm,
    'file:fasta': to_file_fasta,
    'file:bcif': to_file_bcif,
    'molsysmt.MolSys': to_molsysmt_MolSys,
    'molsysmt.Topology': to_molsysmt_Topology,
    'molsysmt.Structures': to_molsysmt_Structures,
    'mdtraj.Trajectory': to_mdtraj_Trajectory,
    'mdtraj.Topology': to_mdtraj_Topology,
    'mmcif.PdbxContainers.DataContainer': to_mmcif_PdbxContainers_DataContainer,
    'openmm.Modeller': to_openmm_Modeller,
    'openmm.Topology': to_openmm_Topology,
    'openmm.PDBFile': to_openmm_PDBFile,
    'string:pdb_text': to_string_pdb_text,
    'nglview.NGLWidget': to_nglview_NGLWidget,
    }
