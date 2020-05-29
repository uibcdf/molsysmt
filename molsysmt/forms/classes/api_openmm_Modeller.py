from os.path import basename as _basename
from simtk.openmm.app.modeller import Modeller as _openmm_Modeller

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Modeller : form_name,
    'openmm.Modeller' : form_name
}

info=["",""]
with_topology=True
with_trajectory=True

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview
    tmp_item = to_mdtraj(item)
    return _mdtraj_to_nglview(tmp_item)

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt import extract as _extract
    import simtk.unit as _unit
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

    tmp_topology = to_mdtraj_Topology(item)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_topology)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = _to_mdtraj_Topology(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_openmm_System(item, atom_indices='all', frame_indices='all'):
    pass

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):
    return item.getTopology()

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    from molsysmt.utils.miscellanea import tmp_filename
    from os import remove
    from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer

    tmp_pdbfile = tmp_filename('pdb')
    to_pdb(item, output_filepath=tmp_pdbfile, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = pdb_to_pdbfixer_PDBFixer(tmp_pdbfile)
    remove(tmp_pdbfile)
    return tmp_item

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):
    from molsysmt.native.io.molsys.classes import from_openmm_Modeller as MolSys_from_openmm_Modeller
    return MolSys_from_openmm_Modeller(item, atom_indices=atom_indices)

def to_pdb(item, output_filepath = None, atom_indices='all', frame_indices='all'):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    from simtk.openmm.version import short_version

    tmp_io = StringIO()
    PDBFile.writeFile(item.topology, item.positions, tmp_io)
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

###### Get

## atom

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_name_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_atom_type_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_groups_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_group_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_aminoacids_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_nucleotides_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_waters_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_ions_from_atom as _get
    _get(item.topology, indices=indices)

def get_mass_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_mass as _get
    return _get(item, indices=indices)

def get_net_mass_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_net_mass as _get
    return _get(item, indices=indices)

def get_charge_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_charge as _get
    return _get(item, indices=indices)

def get_net_charge_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get_degrees_of_freedom_charge as _get
    return _get(item, indices=indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices=indices)

def get_coordinates_from_atom (item, indices='all', frame_indices='all'):

    from numpy import array as _array

    coordinates = _array(item.positions._value)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if indices is not 'all':
        coordinates = coordinates.positions[:,indices,:]

    coordinates = coordinates * item.positions.unit

    return coordinates

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    box = get_box_from_system(item)

    return None, None, coordinates, box

## group

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_groups_from_group as _get
    return _get(item, indices=indices)

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_name_from_group as _get
    return _get(item, indices=indices)

def get_group_index_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_index_from_group as _get
    return _get(item, indices=indices)

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_group_id_from_group as _get
    return _get(item, indices=indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_group as _get
    return _get(item, indices=indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_group as _get
    return _get(item, indices=indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_group as _get
    return _get(item, indices=indices)

## chain

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_index_from_chain as _get
    return _get(item, indices=indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_chain_id_from_chain as _get
    return _get(item, indices=indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_chains_from_chain as _get
    return _get(item, indices=indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_chain as _get
    return _get(item, indices=indices)

## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_system as _get
    return _get(item, indices=indices)

def get_charge_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get_charge as _get
    return _get(item, indices=indices)

def get_net_charge_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get_degrees_of_freedom as _get
    return _get(item, indices=indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_box_from_system as _get

    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    coordinates = _array(item.positions._value)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])
    coordinates = coordinates * item.positions.unit

    return coordinates

def get_frame_from_system (item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    box = get_box_from_system(item)

    return None, None, coordinates, box


def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


