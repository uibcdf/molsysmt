form_name = 'pdbfixer.PDBFixer'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = 'openmm.Topology'
piped_structural_attribute = None
piped_any_attribute = None
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
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
        'pdbfixer.PDBFixer': 'to_pdbfixer_PDBFixer',
        'file:pdb': 'to_file_pdb',
        'string:amino_acids_1': 'to_string_amino_acids_1',
        'string:amino_acids_3': 'to_string_amino_acids_3',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'openmm.Topology': 'to_openmm_Topology',
        'openmm.Modeller': 'to_openmm_Modeller',
        'biopython.Seq': 'to_biopython_Seq',
        'biopython.SeqRecord': 'to_biopython_SeqRecord',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        }
