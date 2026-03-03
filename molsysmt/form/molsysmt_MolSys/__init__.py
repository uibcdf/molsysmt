from .to_openmm_Modeller import to_openmm_Modeller
from .to_networkx_Graph import to_networkx_Graph
from .to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON
from .to_pytraj_Trajectory import to_pytraj_Trajectory
from .to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer
from .to_biopython_SeqRecord import to_biopython_SeqRecord
from .to_file_psf import to_file_psf
from .to_molsysmt_UniversalJSON import to_molsysmt_UniversalJSON
from .to_string_pdb_text import to_string_pdb_text
from .to_pytraj_Topology import to_pytraj_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget
from .to_openmm_Simulation import to_openmm_Simulation
from .to_file_pdb import to_file_pdb
from .to_biopython_Seq import to_biopython_Seq
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanicsDict
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_string_amino_acids_3 import to_string_amino_acids_3
from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
from .to_openmm_Context import to_openmm_Context
from .to_molsysviewer_MolSysView import to_molsysviewer_MolSysView
from .to_openmm_System import to_openmm_System
from .to_parmed_Structure import to_parmed_Structure
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_file_h5msm import to_file_h5msm
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_openmm_Topology import to_openmm_Topology
from .to_XYZ import to_XYZ
from .to_file_msmpk import to_file_msmpk
from .to_molsysmt_Topology import to_molsysmt_Topology
from .add_bonds import add_bonds
from .remove_bonds import remove_bonds

form_name = 'molsysmt.MolSys'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
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
from .get_mechanical_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .add_bonds import add_bonds
from .remove_bonds import remove_bonds

_convert_to={
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'molsysmt.MolecularMechanics': 'to_molsysmt_MolecularMechanics',
        'molsysmt.MolecularMechanicsDict': 'to_molsysmt_MolecularMechanicsDict',
        'networkx.Graph': 'to_networkx_Graph',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        'molsysviewer.MolSysView': 'to_molsysviewer_MolSysView',
        'openmm.Context': 'to_openmm_Context',
        'openmm.Topology': 'to_openmm_Topology',
        'openmm.Modeller': 'to_openmm_Modeller',
        'openmm.System': 'to_openmm_System',
        'openmm.Simulation': 'to_openmm_Simulation',
        'parmed.Structure': 'to_parmed_Structure',
        'pdbfixer.PDBFixer': 'to_pdbfixer_PDBFixer',
        'pytraj.Topology': 'to_pytraj_Topology',
        'pytraj.Trajectory': 'to_pytraj_Trajectory',
        'biopython.Seq': 'to_biopython_Seq',
        'biopython.SeqRecord': 'to_biopython_SeqRecord',
        'biopython.PDBStructure': 'to_biopython_PDBStructure',
        'molsysmt.ViewerJSON': 'to_molsysmt_ViewerJSON',
        'molsysmt.UniversalJSON': 'to_molsysmt_UniversalJSON',
        'rdkit.Mol': 'to_rdkit_Mol',
        'XYZ': 'to_XYZ',
        'string:pdb_text': 'to_string_pdb_text',
        'string:amino_acids_1': 'to_string_amino_acids_1',
        'string:amino_acids_3': 'to_string_amino_acids_3',
        'file:msmpk': 'to_file_msmpk',
        'file:h5msm': 'to_file_h5msm',
        'file:pdb': 'to_file_pdb',
        'file:psf': 'to_file_psf',
        }

_conversion_opt_kwargs={
    'string:pdb_text': ['pdb_chain_id'],
    'pdbfixer.PDBFixer': ['pdb_chain_id']
}
