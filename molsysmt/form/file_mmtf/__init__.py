form_name = 'file:mmtf'
form_type = 'file'
form_info = ["", ""]

from .is_file_mmtf import is_file_mmtf

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj import load_mmtf, MMTFTrajectoryFile

from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_MDAnalysis_Universe import to_MDAnalysis_Universe, _to_MDAnalysis_Universe
from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder, _to_mmtf_MMTFDecoder
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology 
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1 
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3 
from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text 

_dict_convert={
        'file:pdb': _to_file_pdb,
        'mmtf.MMTFDecoder': _to_mmtf_MMTFDecoder,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'openmm.Topology': _to_openmm_Topology,
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids3,
        'string:pdb_text': _to_string_pdb_text,
        }
