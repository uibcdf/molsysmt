form_name = 'mmtf.MMTFDecoder'
form_type = 'class'
form_info = ["", ""]

from .is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_file_mmtf import to_file_mmtf, _to_file_mmtf
from .to_file_pdb import to_file_pdb, _to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3
from .to_string_pdb_text import to_string_pdb_text, _to_string_pdb_text

_dict_convert={
        'file:mmtf': _to_file_mmtf,
        'file:pdb': _to_file_pdb,
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'molsysmt.Structures': _to_molsysmt_Structures,
        'mdtraj.Trajectory': _to_mdtraj_Trajectory,
        'openmm.Topology': _to_openmm_Topology,
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids3,
        'string:pdb_text': _to_string_pdb_text,
        }
