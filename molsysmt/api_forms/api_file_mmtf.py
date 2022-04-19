from molsysmt._private.exceptions import *

from molsysmt.form.file_mmtf.is_file_mmtf import is_file_mmtf as is_form
from molsysmt.form.file_mmtf.extract import extract
from molsysmt.form.file_mmtf.add import add
from molsysmt.form.file_mmtf.append_structures import append_structures
from molsysmt.form.file_mmtf.get import *
from molsysmt.form.file_mmtf.set import *

import numpy as np

form_name='file:mmtf'
form_type='file'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,
    'bond_order' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : False,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield_parameters' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_mmtf_MMTFDecoder as file_mmtf_to_mmtf_MMTFDecoder

    tmp_item = file_mmtf_to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_molsysmt_MolSys as file_mmtf_to_molsysmt_MolSys

    tmp_item = file_mmtf_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_molsysmt_Topology as file_mmtf_to_molsysmt_Topology

    tmp_item = file_mmtf_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_molsysmt_Structures as file_mmtf_to_molsysmt_Structures

    tmp_item = file_mmtf_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_string_aminoacids1 as file_mmtf_to_string_aminoacids1
    from molsysmt.form.file_mmtf import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    tmp_item = file_mmtf_to_string_aminoacids1(item, group_indices=group_indices, check=False)

    return tmp_item

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_string_aminoacids3 as file_mmtf_to_string_aminoacids3
    from molsysmt.form.file_mmtf import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    tmp_item = file_mmtf_to_string_aminoacids3(item, group_indices=group_indices, check=False)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_mdanalysis_Universe as file_mmtf_to_mdanalysis_Universe

    tmp_item = file_mmtf_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.file_mmtf import to_file_pdb as file_mmtf_to_file_pdb

    tmp_item = file_mmtf_to_file_pdb(item, atom_indices=atom_indices,
                                     structure_indices=structure_indices,
                                     output_filename=output_filename, check=False)

    return tmp_item

