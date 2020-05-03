from os.path import basename as _basename
from simtk.openmm.app import Simulation as _openmm_Simulation

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Simulation : form_name,
    'openmm.Simulation' : form_name,
}

info=["",""]

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    tmp_item=item.topology
    tmp_item=extract(atom_indices=atom_indices, frame_indices=frame_indices)
    return item.topology

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import Modeller
    topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    positions = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Modeller(topology, positions)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    from molsysmt.utils.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = pdb_to_pdbfixer_PDBFixer(tmp_file)
    remove(tmp_pdbfile)
    return tmp_item

def to_pdb (item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    topology.setPeriodicBoxVectors(box)
    return _openmm_app_PDBFILE.writeFile(topology, positions, open(output_file_path, 'w'))

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    state = item.context.getState(getPositions=True)
    coordinates = state.getPositions()
    coordinates = coordinates[indices,:]
    return coordinates

## system

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    state = item.context.getState(getPositions=True)
    coordinates = state.getPositions()
    return coordinates

def get_box_from_system(item, indices='all', frame_indices='all'):

    state = item.context.getState()
    box = state.getPeriodicBoxVectors()
    return box

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

