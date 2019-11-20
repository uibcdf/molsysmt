from os.path import basename as _basename
from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_PDBFixer

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _pdbfixer_PDBFixer : form_name
}

## Methods

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):

    tmp_item = to_openm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return ''.join([ r.name for r in tmp_item.groups() ])

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molmodmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids3_to_aminoacids1(tmp_item)
    return tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all'):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_Seq as aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_Seq(tmp_item)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices='all', frame_indices='all'):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_SeqRecord(tmp_item)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology as mdtraj_Topology
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from simtk.unit import nanometers
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory
    tmp_topology = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    coordinates = coordinates.in_units_of(nanometers)._value
    tmp_item = _mdtraj_Trajectory(coordinates, tmp_topology)
    return tmp_item

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import Modeller as openmm_Modeller
    tmp_topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Modeller(tmp_topology, coordinates)
    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import extract_subsystem as extract_openmm_Topology
    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from yank import Topography as yank_Topography
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = yank_Topography(tmp_item)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

def to_pdb(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import PDBFile as openmm_app_PDBFILE
    tmp_topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    return openmm_app_PDBFILE.writeFile(tmp_topology, coordinates, open(output_file_path, 'w'), keepIds=True)

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview as mdtraj_to_nglview
    tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_to_nglview(tmp_item)
    return tmp_item

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        from simtk.openmm.app import Modeller as openmm_Modeller
        from .api_openmm_Topology import extract_subsystem as extract_openmm_Topology
        from .api_openmm_Modeller import to_pdbfixer_PDBFixer as openmm_Modeller_to_pdbfixer_PDBFixer
        tmp_topology = item.topology
        tmp_topology = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
        coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
        tmp_item = openmm_Modeller(tmp_topology, coordinates)
        tmp_item = openmm_Modeller_to_pdbfixer_PDBFixer(tmp_item)
        return tmp_item

def duplicate(item):

    from os import remove
    from molmodmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from molmodmt.utils.pdb import tmp_pdb_filename
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item = pdb_to_pdbfixer_PDBFixer(tmp_file)
    remove(tmp_file)
    return tmp_item

##### Get

## Atom

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

    from molmodmt import get_mass as _get
    return _get(item, indices=indices)

def get_net_mass_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt import get_net_mass as _get
    return _get(item, indices=indices)

def get_charge_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt import get_charge as _get
    return _get(item, indices=indices)
def get_net_charge_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt import get_degrees_of_freedom_charge as _get
    return _get(item, indices=indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices=indices)

def get_coordinates_from_atom (item, indices='all', frame_indices='all'):

    from .api_openmm_Positions import get_coordinates_from_atom as _get
    return _get(item, indices=indices)

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

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_molecule_type_from_chain as _get
    return _get(item, indices=indices)

## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from .api_openmm_Topology import get_n_atoms_from_system as _get
    return _get(item, indices=indices)

def get_charge_from_system (item, indices='all', frame_indices='all'):

    from molmodmt import get_charge as _get
    return _get(item, indices=indices)

def get_net_charge_from_system (item, indices='all', frame_indices='all'):

    from molmodmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_system (item, indices='all', frame_indices='all'):

    from molmodmt import get_degrees_of_freedom as _get
    return _get(item, indices=indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)


##### Set

def set_name_to_group(item, indices='all', frame_indices='all', value=None):
    for group in tmp_item.topology.groups():
        if group.index in indices:
            name = value[np.where(indices == group.index)[0][0]]
            group.name = name
    for bond in tmp_item.topology.bonds():
        for ii in [0,1]:
            if bond[ii].group.index in set_indices:
                name = kwargs[option][np.where(array_indices == bond[ii].group.index)[0][0]]
                bond[ii].group.name = name

