form_name = 'file:top'
form_type = 'file'
form_info = ["GROMACS topology file format",
             "https://manual.gromacs.org/current/reference-manual/file-formats.html#top"]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
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
from .iterators import TopologyIterator


_convert_to={
        'file:top': 'to_file_top',
        'parmed.GromacsTopologyFile': 'to_parmed_GromacsTopologyFile',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        }
