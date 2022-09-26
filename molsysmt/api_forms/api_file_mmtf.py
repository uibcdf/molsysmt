from molsysmt.form.file_mmtf.is_file_mmtf import is_file_mmtf as is_form
from molsysmt.form.file_mmtf.extract import extract
from molsysmt.form.file_mmtf.add import add
from molsysmt.form.file_mmtf.append_structures import append_structures
from molsysmt.form.file_mmtf.get import *
from molsysmt.form.file_mmtf.set import *
from .form_attributes import form_attributes

import numpy as np

form_name = 'file:mmtf'
form_type = 'file'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['box'] = True
form_attributes['forcefield_parameters'] = True


def to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_mmtf_MMTFDecoder as file_mmtf_to_mmtf_MMTFDecoder

    return file_mmtf_to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_molsysmt_MolSys as file_mmtf_to_molsysmt_MolSys

    return file_mmtf_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_molsysmt_Topology as file_mmtf_to_molsysmt_Topology

    return file_mmtf_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_molsysmt_Structures as file_mmtf_to_molsysmt_Structures

    return file_mmtf_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_openmm_Topology as file_mmtf_to_openmm_Topology

    return file_mmtf_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_string_aminoacids1 as file_mmtf_to_string_aminoacids1
    from molsysmt.form.file_mmtf import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    return file_mmtf_to_string_aminoacids1(item, group_indices=group_indices)


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_string_aminoacids3 as file_mmtf_to_string_aminoacids3
    from molsysmt.form.file_mmtf import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    return file_mmtf_to_string_aminoacids3(item, group_indices=group_indices)


def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_mdanalysis_Universe as file_mmtf_to_mdanalysis_Universe

    return file_mmtf_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.file_mmtf import to_file_pdb as file_mmtf_to_file_pdb

    return file_mmtf_to_file_pdb(item, atom_indices=atom_indices,
                                     structure_indices=structure_indices,
                                     output_filename=output_filename)

def to_string_pdb_text(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_mmtf import to_string_pdb_text as file_mmtf_to_string_pdb_text

    return file_mmtf_to_string_pdb_text(item, atom_indices=atom_indices,
                                        structure_indices=structure_indices)

