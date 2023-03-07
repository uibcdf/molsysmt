form_name = 'molsysmt.MolecularMechanics'
form_type = 'class'
form_info = ["", ""]

from .is_molsysmt_MolecularMechanics import is_molsysmt_MolecularMechanics

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict, _to_molsysmt_MolecularMechanicsDict

_convert_to={
        'molsysmt.MolecularMechanicsDict': _to_molsysmt_MolecularMechanicsDict,
        }
