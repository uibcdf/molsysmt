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

from .to_file_pdb import to_file_pdb
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_string_amino_acids_3 import to_string_amino_acids_3
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller
from .to_biopython_Seq import to_biopython_Seq
from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'pdbfixer.PDBFixer': extract,
        'file:pdb': to_file_pdb,
        'string:amino_acids_1': to_string_amino_acids_1,
        'string:amino_acids_3': to_string_amino_acids_3,
        'molsysmt.MolSys': to_molsysmt_MolSys,
        'molsysmt.Topology': to_molsysmt_Topology,
        'molsysmt.Structures': to_molsysmt_Structures,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'mdtraj.Trajectory': to_mdtraj_Trajectory,
        'mdtraj.Topology': to_mdtraj_Topology,
        'openmm.Topology': to_openmm_Topology,
        'openmm.Modeller': to_openmm_Modeller,
        'biopython.Seq': to_biopython_Seq,
        'biopython.SeqRecord': to_biopython_SeqRecord,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
