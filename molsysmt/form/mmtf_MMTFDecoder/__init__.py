form_name = 'mmtf.MMTFDecoder'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'

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

from .to_file_mmtf import to_file_mmtf
from .to_file_pdb import to_file_pdb
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_openmm_Topology import to_openmm_Topology
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3
from .to_string_pdb_text import to_string_pdb_text

_convert_to={
        'mmtf.MMTFDecoder': extract,
        'file:mmtf': to_file_mmtf,
        'file:pdb': to_file_pdb,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'openmm.Topology': to_openmm_Topology,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids3,
        'string:pdb_text': to_string_pdb_text,
        }
