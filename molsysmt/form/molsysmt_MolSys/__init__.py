form_name = 'molsysmt.MolSysNEW'
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

from .to_molsysmt_TopologyNEW import to_molsysmt_TopologyNEW
from .to_molsysmt_StructuresNEW import to_molsysmt_StructuresNEW
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict
from .to_file_msmpk import to_file_msmpk

_convert_to={
        'molsysmt.MolSysNEW': extract,
        'molsysmt.TopologyNEW': to_molsysmt_TopologyNEW,
        'molsysmt.StructuresNEW': to_molsysmt_StructuresNEW,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'molsysmt.MolecularMechanicsDict': to_molsysmt_MolecularMechanicsDict,
        'file:msmpk': to_file_msmpk,
        }

