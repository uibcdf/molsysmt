form_name = 'openff.Molecule'
form_type = 'class'
form_info = ["OpenFF Toolkit Molecule", "https://docs.openforcefield.org/projects/toolkit/"]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_openff_Topology import to_openff_Topology
from .to_rdkit_Mol import to_rdkit_Mol
from .to_string_smiles import to_string_smiles

_convert_to = {
    'molsysmt.Topology': to_molsysmt_Topology,
    'molsysmt.Structures': to_molsysmt_Structures,
    'molsysmt.MolSys': to_molsysmt_MolSys,
    'openff.Topology': to_openff_Topology,
    'rdkit.Mol': to_rdkit_Mol,
    'string:smiles': to_string_smiles,
}

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator
