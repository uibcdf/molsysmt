from os.path import basename as _basename
from simtk.openmm.app.modeller import Modeller as _openmm_Modeller
import simtk.unit as unit

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Modeller : form_name,
    'openmm.Modeller' : form_name
}

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_parameters=False

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt import extract as _extract
    import simtk.unit as _unit
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

    tmp_topology = to_mdtraj_Topology(item)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_topology)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from .api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = _to_mdtraj_Topology(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_openmm_System(item, atom_indices='all', frame_indices='all',
                     topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=1.0*unit.nanometer, constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from .api_openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, atom_indices='all', forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, **kwargs)

    return tmp_item

def to_openmm_Simulation(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=1.0*unit.nanometer, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature=300.0*unit.kelvin,
                         collisions_rate=1.0/unit.picoseconds, integration_timestep=2.0*unit.femtoseconds, platform='CUDA'):

    from .api_openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation
    from molsysmt import get

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)

    if trajectory_item is None:
        positions = get(item, target='atom', indices=atom_indices, frame_indices=frame_indices, coordinates=True)
    else:
        positions = get(trajectory_item, target='atom', indices=atom_indices, frame_indices=frame_indices, coordinates=True)

    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, trajectory_item=positions, atom_indices='all', forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, integrator=integrator, temperature=temperature,
                                                collisions_rate=collisions_rate, platform=platform, **kwargs)

    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from .api_openmm_Topology import extract as extract_openmm_Topology

    tmp_item = item.getTopology()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from io import StringIO
    from pdbfixer.pdbfixer import PDBFixer

    tmp_item = to_pdb(item, output_filename='.pdb', atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):


    from molsysmt.native.io.molsys.classes import from_openmm_Modeller as MolSys_from_openmm_Modeller
    return MolSys_from_openmm_Modeller(item, atom_indices=atom_indices)

def to_pdb(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
           output_filename = None):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    #from simtk.openmm.version import short_version
    from molsysmt import __version__ as msm_version
    from simtk.openmm import Platform # the openmm version is taken from this module (see: simtk/openmm/app/pdbfile.py)

    tmp_io = StringIO()
    PDBFile.writeFile(item.topology, item.positions, tmp_io, keepIds=True)
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

def select_with_MDTraj(item, selection):

    tmp_item = to_mdtraj_Topology(item)
    return tmp_item.select(selection)

def copy(item):

    from simtk.openmm.app import Modeller as _Modeller

    tmp_item = _Modeller(item.topology, item.positions)
    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from api_openmm_Topology import extract_atom_indices as _extract_topology

        tmp_item = copy(item)
        tmp_item.topology = _extract_topology(item.topology, atom_indices)
        tmp_item.positions = get_coordinates_from_atom(item, atom_indices)

        return tmp_item

def merge_two_items(item1, item2):

    from .api_mdtraj_Trajectory import to_openmm_Modeller as _from_mdtraj_Trajectory
    tmp_item1 = to_mdtraj(item1)
    tmp_item2 = to_mdtraj(item2)
    tmp_item = tmp_item1.stack(tmp_item2)
    tmp_item = _from_mdtraj_Trajectory(tmp_item)

    #from molsysmt import copy as _copy, get as _get
    #tmp_item = copy(item1)
    #topology2 = to_openmm_Topology(item2)
    #positions2 = _get(item2, coordinates=True)
    #tmp_item = tmp_item.add(topology2, positions2)

    return tmp_item

def view_with_NGLView(item, atom_indices='all', frame_indices='all'):

    from .api_molsysmt_MolSys import to_NGLView as _molsysmt_MolSys_to_NGLView
    tmp_item = to_molsysmt_MolSys(item)
    return _molsysmt_MolSys_view_with_NGLView(tmp_item)

###### Get

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

def get_coordinates_from_atom (item, indices='all', frame_indices='all'):

    from numpy import array as _array

    coordinates = _array(item.positions._value)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if frame_indices is not 'all':
        coordinates = coordinates[frame_indices,:,:]

    if indices is not 'all':
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * item.positions.unit

    return coordinates

def get_frame_from_atom (item, indices='all', frame_indices='all'):

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

    from numpy import array as _array

    coordinates = _array(item.positions._value)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])
    if frame_indices is not 'all':
        coordinates = coordinates[frame_indices,:,:]
    coordinates = coordinates * item.positions.unit

    return coordinates

def get_box_from_system(item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_box_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_box_shape_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_box_lengths_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_box_angles_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array
    from simtk.unit import picoseconds

    n_frames = get_n_frames_from_system(item)
    output = [None for ii in range(n_frames)]
    output = _array(output)*picoseconds
    return output

def get_step_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array
    n_frames = get_n_frames_from_system(item)
    output = [None for ii in range(n_frames)]
    output = _array(output)
    return output

def get_frame_from_system (item, indices='all', frame_indices='all'):

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


