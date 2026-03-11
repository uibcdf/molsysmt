from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_file_trjpk import to_file_trjpk
from .to_file_structures_yaml import to_file_structures_yaml
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology
form_name='molsysmt.StructuresDict'
form_type='class'
form_info = ["",""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False


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
from .iterators import StructuresIterator


_convert_to={
        'molsysmt.StructuresDict': to_molsysmt_StructuresDict,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'file:trjpk': to_file_trjpk,
        'file:structures_yaml': to_file_structures_yaml,
        }
