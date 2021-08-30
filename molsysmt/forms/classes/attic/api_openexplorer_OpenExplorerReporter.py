from os.path import basename as _basename
from openexplorer.reporters import OpenExplorerReporter as _openexplorer_OpenExplorerReporter
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openexplorer_OpenExplorerReporter : form_name
}

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_parameters=True

## Methods

def to_openmm_Topology(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from .api_openmm_Topology import extract
    tmp_item = item.topology
    tmp_item = extract(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import from_openexplorer_OpenExplorerReporter as convert
    return convert(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
                           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.classes import from_openexplorer_OpenExplorerReporter as convert
    return convert(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_openexplorer_OpenExplorerReporter as convert
    return convert(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_pdb(item,  atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
           output_filename=None):

    from io import StringIO
    from openmm.app import PDBFile
    from openmm.version import short_version
    from molsysmt import __version__ as msm_version
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)

    tmp_io = StringIO()
    positions = get_coordinates_from_system(item, atom_indices=atom_indices, frame_indices=frame_indices)[0]
    topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    PDBFile.writeFile(topology, positions, tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    if output_filename=='.pdb':
        return filedata
    else:
        with open(output_filename, 'w') as file:
            file.write(filedata)
        pass

def view_with_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as convert
    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return convert(tmp_item)

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select
    tmp_item = to_molsysmt_Topology(item)
    return select(tmp_item, selection)

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

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_id_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_name_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_type_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_id_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_name_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_id_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_type_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_name_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_id_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_type_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_id_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_name_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_id_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_name_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_type_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_bonded_atoms_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bonded_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_bonded_index_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_inner_bonded_atoms_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_inner_bonds_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_atom as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    units = item.coordinates.unit
    coordinates = np.array(item.coordinates._value, dtype=float)
    if indices is not 'all':
        coordinates = coordinates[:, indices, :]
    if frame_indices is not 'all':
        coordinates = coordinates[frame_indices, :, :]
    coordinates = coordinates*units
    return coordinates

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)

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

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_id_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_name_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_type_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_index_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_id_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_name_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_index_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_id_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_type_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_name_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_index_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_id_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_type_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_id_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_name_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_index_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_id_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_name_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_type_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_group as _get
    tmp_item = to_molsysmt_Topology(item)
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

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_id_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_name_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_type_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_index_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_id_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_name_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_index_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_id_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_type_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_name_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_index_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_id_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_type_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_id_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_name_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_index_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_id_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_name_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_type_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_component as _get
    tmp_item = to_molsysmt_Topology(item)
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

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_id_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_name_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_type_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_index_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_id_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_name_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_index_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_id_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_type_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_name_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_index_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_id_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_type_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_id_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_name_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_index_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_id_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_name_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_type_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_molecule as _get
    tmp_item = to_molsysmt_Topology(item)
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

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_id_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_name_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_type_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_index_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_id_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_name_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_index_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_id_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_type_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_name_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_index_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_id_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_type_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_id_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_name_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_index_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_id_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_name_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_type_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_chain as _get
    tmp_item = to_molsysmt_Topology(item)
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

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_id_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_name_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_type_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_index_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_id_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_name_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_index_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_id_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_component_type_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_name_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_index_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_id_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_chain_type_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_id_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_name_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_index_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_id_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_name_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_entity_type_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_entity as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_bonded_atoms_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_chains_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_molecules_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_entities_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_aminoacids_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_nucleotides_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_ions_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_waters_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_cosolutes_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_small_molecules_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_peptides_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_proteins_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_dnas_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_rnas_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_mass_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_charge_from_system as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    return get_coordinates_from_atom(item, indices='all', frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.box is not None:
        units = item.box.unit
        output = np.array(item.box._value, dtype=float)
        if frame_indices is not 'all':
            output = output[frame_indices, :, :]
        output = output*units

    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_time_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.time is not None:
        units = item.time.unit
        output = np.array(item.time._value, dtype=float)
        if frame_indices is not 'all':
            output = output[frame_indices]
        output = output*units

    return output

def get_step_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.step is not None:
        output = np.array(item.step, dtype=int)
        if frame_indices is not 'all':
            output = output[frame_indices]

    return time

def get_frame_from_system(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':

        output=len(item.coordinates)

    else:

        output = frame_indices.shape[0]

    return output

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

## bond

def get_index_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_index_from_bond(item, indices=indices)

def get_order_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_order_from_bond(item, indices=indices)

def get_type_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_type_from_bond(item, indices=indices)

def get_bond_index_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_bond_index_from_bond as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_bond_order_from_bond as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_bond_type_from_bond as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_bond as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import get_n_bonds_from_bond as _get
    tmp_item = to_molsysmt_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

##### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

