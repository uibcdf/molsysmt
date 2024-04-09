form_name = 'openmm.Simulation'
form_type = 'class'
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

from .to_file_pdb import to_file_pdb
from .to_file_msmpk import to_file_msmpk
from .to_openmm_Context import to_openmm_Context
from .to_openmm_Topology import to_openmm_Topology
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_openmm_Modeller import to_openmm_Modeller
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer

_convert_to={
        'openmm.Simulation': extract,
        'file:pdb': to_file_pdb,
        'file:msmpk': to_file_msmpk,
        'openmm.Context': to_openmm_Context,
        'openmm.Topology': to_openmm_Topology,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'openmm.Modeller': to_openmm_Modeller,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        }
