from molsysmt.item.openmm_GromacsGroFile.is_openmm_GromacsGroFile import is_openmm_GromacsGroFile as is_form
from molsysmt.item.openmm_GromacsGroFile.extract import extract
from molsysmt.item.openmm_GromacsGroFile.add import add
from molsysmt.item.openmm_GromacsGroFile.append_structures import append_structures
from molsysmt.item.openmm_GromacsGroFile.get import *
from molsysmt.item.openmm_GromacsGroFile.set import *
from .form_attributes import form_attributes

form_name = 'openmm.GromacsGroFile'
form_type = 'class'
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
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    return openmm_GromacsGroFile_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_GromacsGroFile import to_openmm_Modeller as openmm_GromacsGroFile_to_openmm_Modeller

    return openmm_GromacsGroFile_to_openmm_Modeller(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_GromacsGroFile import to_molsysmt_MolSys as openmm_GromacsGroFile_to_molsysmt_MolSys

    return openmm_GromacsGroFile_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_GromacsGroFile import to_molsysmt_Topology as openmm_GromacsGroFile_to_molsysmt_Topology

    return openmm_GromacsGroFile_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_GromacsGroFile import \
        to_molsysmt_Structures as openmm_GromacsGroFile_to_molsysmt_Structures

    return openmm_GromacsGroFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                        structure_indices=structure_indices)
