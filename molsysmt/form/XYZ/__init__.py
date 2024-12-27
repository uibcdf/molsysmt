form_name = 'XYZ'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

from .is_form import is_form
from .get_rank_3_XYZ import get_rank_3_XYZ

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

from .to_file_xyznpy import to_file_xyznpy
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics

_convert_to={
        'XYZ': extract,
        'file:xyznpy': to_file_xyznpy,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        }
