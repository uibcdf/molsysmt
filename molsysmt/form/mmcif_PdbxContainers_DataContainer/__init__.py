form_name = 'mmcif.PdbxContainers.DataContainer'
form_type = 'class'
form_info = ["", ""]

# https://mmcif.wwpdb.org/
# https://github.com/rcsb/py-mmcif

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
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
    'mmcif.PdbxContainers.DataContainer': 'to_mmcif_PdbxContainers_DataContainer',
    'file:pdb': 'to_file_pdb',
    'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'molsysmt.MolecularMechanics': 'to_molsysmt_MolecularMechanics',
    'openmm.Topology': 'to_openmm_Topology',
    'string:amino_acids_1': 'to_string_amino_acids_1',
    'string:amino_acids_3': 'to_string_amino_acids_3',
    'string:pdb_text': 'to_string_pdb_text',
    'string:pdb_id': 'to_string_pdb_id',
    }

