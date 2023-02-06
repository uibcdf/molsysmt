from molsysmt.form.file_h5.is_file_h5 import is_file_h5 as is_form
from molsysmt.form.file_h5.extract import extract
from molsysmt.form.file_h5.add import add
from molsysmt.form.file_h5.append_structures import append_structures
from molsysmt.form.file_h5.get import *
from molsysmt.form.file_h5.set import *
from molsysmt.form.file_h5.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name='file:crd'
form_type = 'file'
info = ["CHARMM card (CRD) file format with coordinates.","https://www.charmmtutorial.org/index.php/CHARMM:The_Basics#CHARMM_data_structures"]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = False
form_attributes['bond_id'] = False
form_attributes['bond_name'] = False
form_attributes['bond_type'] = False
form_attributes['bond_order'] = False
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = False
form_attributes['molecule_index'] = False
form_attributes['molecule_id'] = False
form_attributes['molecule_name'] = False
form_attributes['molecule_type'] = False
form_attributes['chain_index'] = False
form_attributes['chain_id'] = False
form_attributes['chain_name'] = False
form_attributes['chain_type'] = False
form_attributes['coordinates'] = True
form_attributes['velocities'] = False
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['structure_id'] = True
form_attributes['forcefield_parameters'] = False
form_attributes['temperature'] = False


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_molsysmt_MolSys as file_crd_to_molsysmt_MolSys

    tmp_item = file_crd_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_molsysmt_MolSys as file_crd_to_molsysmt_Topology

    tmp_item = file_crd_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_molsysmt_Structures as file_crd_to_molsysmt_Structures

    tmp_item = file_crd_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_mdanalysis_Universe as file_crd_to_mdanalysis_Universe

    tmp_item = file_crd_to_mdanalysis_Universe(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_mdanalysis_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_mdanalysis_Topology as file_crd_to_mdanalysis_Topology

    tmp_item = file_crd_to_mdanalysis_Universe(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_mdanalysis_topology_CRDParser(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_mdanalysis_topology_CRDParser as file_crd_to_mdanalysis_topology_CRDParser

    tmp_item = file_crd_to_mdanalysis_topology_CRDParser(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_mdanalysis_coordinates_CRDReader(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_mdanalysis_coordinates_CRDParser as file_crd_to_mdanalysis_coordinates_CRDParser

    tmp_item = file_crd_to_mdanalysis_coordinates_CRDParser(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_mdtraj_AmberRestartFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_mdtraj_AmberRestartFile as file_crd_to_mdtraj_AmberRestartFile

    tmp_item = file_crd_to_mdtraj_AmberRestartFile(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_openmm_AmberInpcrdFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_crd import to_mdtraj_AmberInpcrdFile as file_crd_to_mdtraj_AmberInpcrdFile

    tmp_item = file_crd_to_mdtraj_AmberInpcrdFile(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

