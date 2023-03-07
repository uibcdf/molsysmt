form_name = 'molsysmt.MolecularMechanicsDict'
form_type = 'class'
form_info = ["", ""]

from .is_molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics, _to_molsysmt_MolecularMechanics

_convert_to={
        'molsysmt.MolecularMechanics': _to_molsysmt_MolecularMechanics,
        }
