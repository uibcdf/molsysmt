form_name='molsysmt.StructuresDict'
form_type='class'
form_info = ["",""]

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

from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_file_trjpk import to_file_trjpk

_convert_to={
        'molsysmt.StructuresDict': extract,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'file:trjpk': to_file_trjpk,
        }
