form_name = 'string:uniprot_id'
form_type = 'string'
form_info = ["UniProt accession number string",
             "https://www.uniprot.org/"]

piped_topological_attribute = 'molsysmt.Topology'
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
from .iterators import TopologyIterator


_convert_to={
        'string:uniprot_id': 'to_string_uniprot_id',
        'file:fasta': 'to_file_fasta',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        }
