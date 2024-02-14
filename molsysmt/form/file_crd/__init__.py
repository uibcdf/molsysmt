form_name='file:crd'
form_type = 'file'
form_info = ["CHARMM card (CRD) file format with coordinates.","https://www.charmmtutorial.org/index.php/CHARMM:The_Basics#CHARMM_data_structures"]

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

from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_openmm_CharmmCrdFile import to_openmm_CharmmCrdFile

_convert_to={
        'file:crd': extract,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'openmm.CharmmCrdFile': to_openmm_CharmmCrdFile
        }
