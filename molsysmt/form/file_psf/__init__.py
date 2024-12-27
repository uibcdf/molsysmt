form_name='file:psf'
form_type = 'file'
form_info = ["CHARMM Protein Structure File (PSF).","https://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node23.html"]

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
from .get import *
from .set import *
from .iterators import TopologyIterator

from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_openmm_CharmmPsfFile import to_openmm_CharmmPsfFile
from .to_openmm_Topology import to_openmm_Topology

_convert_to={
        'file:psf': extract,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'openmm.CharmPsfFile': to_openmm_CharmmPsfFile,
        'openmm.Topology': to_openmm_Topology,
        }

