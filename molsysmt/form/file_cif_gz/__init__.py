from .download import download

form_name = 'file:cif.gz'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = True

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

from .download import download


_convert_to={
    'file:cif.gz': 'to_file_cif_gz',
    'mmcif.PdbxContainers.DataContainer': 'to_mmcif_PdbxContainers_DataContainer',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'file:h5msm': 'to_file_h5msm',
    }

