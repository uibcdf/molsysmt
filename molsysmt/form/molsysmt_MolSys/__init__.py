form_name = 'molsysmt.MolSys'
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
from .get_topological_attributes import *
from .get_structural_attributes import *
from .get_mechanical_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict
from .to_networkx_Graph import to_networkx_Graph
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_openmm_Topology import to_openmm_Topology
from .to_file_msmpk import to_file_msmpk
from .to_file_h5msm import to_file_h5msm
from .to_string_pdb_text import to_string_pdb_text

_convert_to={
        'molsysmt.MolSys': extract,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolecularMechanics': to_molsysmt_MolecularMechanics,
        'molsysmt.MolecularMechanicsDict': to_molsysmt_MolecularMechanicsDict,
        'networkx.Graph': to_networkx_Graph,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        'file:msmpk': to_file_msmpk,
        'file:h5msm': to_file_h5msm,
        'openmm.Topology': to_openmm_Topology,
        'string:pdb_text': to_string_pdb_text,
        }


