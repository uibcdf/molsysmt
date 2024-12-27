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
from .get import *
from .set import *
from .iterators import StructuresIterator

from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_file_trjpk import to_file_trjpk

_convert_to={
        'molsysmt.StructuresDict': extract,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'file:trjpk': to_file_trjpk,
        }
