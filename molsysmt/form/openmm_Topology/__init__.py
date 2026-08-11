from .write_topology_in_h5msm import write_topology_in_h5msm

form_name = 'openmm.Topology'
form_type = 'class'
form_info = ["", ""]

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

from .write_topology_in_h5msm import write_topology_in_h5msm


_convert_to={
        'openmm.Topology': 'to_openmm_Topology',
        'string:pdb_text': 'to_string_pdb_text',
        'file:pdb': 'to_file_pdb',
        'file:psf': 'to_file_psf',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'networkx.Graph': 'to_networkx_Graph',
        'openmm.Modeller': 'to_openmm_Modeller',
        'openmm.Simulation': 'to_openmm_Simulation',
        'openmm.Context': 'to_openmm_Context',
        'openmm.PDBFile': 'to_openmm_PDBFile',
        'openmm.System': 'to_openmm_System',
        'parmed.Structure': 'to_parmed_Structure',
        'pdbfixer.PDBFixer': 'to_pdbfixer_PDBFixer',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        'string:amino_acids_1': 'to_string_amino_acids_1',
        'string:amino_acids_3': 'to_string_amino_acids_3',
        }

_conversion_opt_kwargs={
        'openmm.Simulation': ['collisions_rate', 'integration_timestep'],
        }
