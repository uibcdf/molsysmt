form_name = 'openmm.Simulation'
form_type = 'class'
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
from .to_file_msmpk import to_file_msmpk
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_openmm_Context import to_openmm_Context
from .to_openmm_Topology import to_openmm_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_openmm_Modeller import to_openmm_Modeller
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer

_convert_to={
        'openmm.Simulation': extract,
        'file:pdb': to_file_pdb,
        'file:msmpk': to_file_msmpk,
        'molsysmt.Topology': to_molsysmt_Topology,
        'openmm.Context': to_openmm_Context,
        'openmm.Topology': to_openmm_Topology,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Structures': to_molsysmt_Structures,
        'openmm.Modeller': to_openmm_Modeller,
        'pdbfixer.PDBFixer': to_pdbfixer_PDBFixer,
        }
