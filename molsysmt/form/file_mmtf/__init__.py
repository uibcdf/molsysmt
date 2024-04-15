form_name = 'file:mmtf'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

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

from .to_mdtraj import load_mmtf, MMTFTrajectoryFile

from .to_file_pdb import to_file_pdb
from .to_MDAnalysis_Universe import to_MDAnalysis_Universe
from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_openmm_Topology import to_openmm_Topology
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_string_amino_acids_3 import to_string_amino_acids_3
from .to_string_pdb_text import to_string_pdb_text

_convert_to={
        'file:mmtf': extract,
        'file:pdb': to_file_pdb,
        'mmtf.MMTFDecoder': to_mmtf_MMTFDecoder,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'openmm.Topology': to_openmm_Topology,
        'string:amino_acids_1': to_string_amino_acids_1,
        'string:amino_acids_3': to_string_amino_acids_3,
        'string:pdb_text': to_string_pdb_text,
        }
