from os.path import basename as _basename
from openexplorer import Explorer as _openexplorer_Explorer

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openexplorer_Explorer : form_name
}

info=["",""]
with_topology=True
with_trajectory=True

## Methods

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import extract as extract_openmm_Topology
    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return item.topology

def to_openmm_Context(item, atom_indices='all', frame_indices='all'):

    return item.context

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openexplorer_Explorer as molsysmt_Topology_from_openexplorer_Explorer
    return molsysmt_Topology_from_openexplorer_Explorer(item, atom_indices=atom_indices)

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_openexplorer_Explorer as molsysmt_Trajectory_from_openexplorer_Explorer
    return molsysmt_Trajectory_from_openexplorer_Explorer(item, atom_indices=atom_indices)

def to_molsysmt_System(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_openexplorer_Explorer as molsysmt_System_from_openexplorer_Explorer
    return molsysmt_System_from_openexplorer_Explorer(item, atom_indices=atom_indices)

def to_pdb(item, output_filepath=None, atom_indices='all', frame_indices='all'):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    from simtk.openmm.version import short_version

    tmp_io = StringIO()
    positions = get_coordinates_from_system(item)
    PDBFile.writeFile(item.topology, positions, tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    filedata = filedata.replace('WITH OPENMM '+short_version, 'WITH OPENMM '+short_version+' BY MOLSYSMT')
    tmp_io.close()
    del(tmp_io)

    if output_filepath=='.pdb':
        return filedata
    else:
        with open(output_filepath, 'w') as file:
            file.write(filedata)
        pass

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_nglview as molsysmt_MolSys_to_nglview

    return molsysmt_MolSys_to_nglview(item, atom_indices=atom_indices, frame_indices=frame_indices)

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_molsysmt_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_molsysmt_Topology_with_MolSysMT(tmp_item, selection)

##### Get

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bonded_atoms_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_coordinates_from_atom as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    return get_n_frames_from_system(item, frame_indices=frame_indices)

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bonded_atoms_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_aminoacids_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_nucleotides_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_ions_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_waters_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_cosolutes_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_small_molecules_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_peptides_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_proteins_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_dnas_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_rnas_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_coordinates_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_shape_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_lengths_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_angles_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_time_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_step_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_step_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_frame_from_system(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':

        return 1

    else:

        output = frame_indices.shape[0]
        if output>1:
            raise ValueError('The molecular system has a single frame')
        return output

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

##### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    from molsysmt.forms.classes.api_openmm_Context import set_box_to_system as _set
    return _set(item.context, indices=indices, frame_indices=frame_indices, value=value)

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    from molsysmt.forms.classes.api_openmm_Context import set_coordinates_to_system as _set
    return _set(item.context, indices=indices, frame_indices=frame_indices, value=value)

