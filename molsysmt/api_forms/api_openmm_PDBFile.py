from molsysmt._private.exceptions import *

from molsysmt.form.openmm_PDBFile.is_openmm_PDBFile import is_openmm_PDBFile as is_form
from molsysmt.form.openmm_PDBFile.extract import extract
from molsysmt.form.openmm_PDBFile.add import add
from molsysmt.form.openmm_PDBFile.merge import merge
from molsysmt.form.openmm_PDBFile.append_structures import append_structures
from molsysmt.form.openmm_PDBFile.concatenate_structures import concatenate_structures
from molsysmt.form.openmm_PDBFile.get import *
from molsysmt.form.openmm_PDBFile.set import *

form_name='openmm.PDBFile'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : True,
    'component_name' : True,
    'component_type' : True,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : True,
    'entity_id' : True,
    'entity_name' : True,
    'entity_type' : True,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,

}

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = openmm_PDBFile_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_Structures as openmm_PDBFile_to_molsysmt_Structures

    tmp_item = openmm_PDBFile_to_molsysmt_Structures(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_MolSys as openmm_PDBFile_to_molsysmt_MolSys

    tmp_item = openmm_PDBFile_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_mdtraj_Trajectory as openmm_PDBFile_to_mdtraj_Trajectory

    tmp_item = openmm_PDBFile_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_mdtraj_Topology as openmm_PDBFile_to_mdtraj_Topology

    tmp_item = openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_Topology as openmm_PDBFile_to_mdtraj_Topology

    tmp_item = openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_nglview_NGLWidget as openmm_Topology_to_nglview_NGLWidget

    tmp_item = openmm_Topology_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        from copy import copy
        tmp_item = copy(item)
    else:
        from molsysmt.api_forms.api_openmm_Topology import extract as extract_openmm_Topology
        from molsysmt import convert
        if atom_indices is not 'all':
            topology = extract_openmm_Topology(item.topology, atom_indices=atom_indices)
        else:
            topology = item.topology
        coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
        tmp_item = convert([topology, coordinates], to_form='openmm.PDBFile')

    return tmp_item


###### Get

def aux_get(item, indices='all', structure_indices='all'):


    tmp_item, _ = to_openmm_Topology(item)
    method_name = sys._getframe(1).f_code.co_name
    module = importlib.import_module('molsysmt.api_forms.api_openmm_Topology')
    _get = getattr(module, method_name)

    output = _get(tmp_item, indices=indices, structure_indices=structure_indices)

    return output

## atom

def get_atom_index_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    if structure_indices is 'all':

        n_structures = get_n_structures_from_system(item)
        structure_indices = np.arange(n_structures)

    output = []

    for frame_index in structure_indices:
        tmp_coordinates = item.getPositions(asNumpy=True, frame=frame_index)
        tmp_unit = tmp_coordinates.unit
        if indices is 'all':
            output.append(tmp_coordinates._value)
        else:
            output.append(tmp_coordinates[indices,:]._value)

    output = np.array(output)*tmp_unit

    return output

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    step = get_step_from_system(item, structure_indices=structure_indices)
    time = get_time_from_system(item, structure_indices=structure_indices)

    return step, time, coordinates, box

## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## component

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_coordinates_from_system(item, indices='all', structure_indices='all'):

    return get_coordinates_from_atom(item, indices='all', structure_indices=structure_indices)

def get_box_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_time_from_system(item, indices='all', structure_indices='all'):

    from numpy import array as _array
    from openmm.unit import picoseconds

    n_structures = get_n_structures_from_system(item)
    output = [None for ii in range(n_structures)]
    output = _array(output)*picoseconds
    return output

def get_step_from_system(item, indices='all', structure_indices='all'):

    from numpy import array as _array
    n_structures = get_n_structures_from_system(item)
    output = [None for ii in range(n_structures)]
    output = _array(output)
    return output

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    if structure_indices is 'all':

        return item.getNumFrames()

    else:

        output = structure_indices.shape[0]
        if output>1:
            raise ValueError('The molecular system has a single frame')
        return output

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    return aux_get(item, indices=indices, structure_indices=structure_indices)

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

