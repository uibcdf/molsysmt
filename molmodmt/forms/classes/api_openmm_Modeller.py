from os.path import basename as _basename
from simtk.openmm.app.modeller import Modeller as _openmm_Modeller

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Modeller : form_name,
    'openmm.Modeller' : form_name
}

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview
    tmp_item = to_mdtraj(item)
    return _mdtraj_to_nglview(tmp_item)

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    import simtk.unit as _unit
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

    tmp_topology = to_mdtraj_Topology(item)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_topology)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)

    return tmp_item

def to_mdtraj_Topology(item, selection=None, syntaxis='mdtraj'):

    from .api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = _to_mdtraj_Topology(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_openmm_System(item, selection=None, syntaxis='mdtraj'):
    pass

def to_openmm_Topology(item, selection=None, syntaxis='mdtraj'):
    return item.getTopology()

def to_pdbfixer_PDBFixer(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.utils.miscellanea import tmp_filename
    from os import remove
    from molmodmt import convert

    tmp_pdbfile = tmp_filename('pdb')
    to_pdb(item, tmp_pdbfile)
    tmp_item = convert(tmp_pdbfile, 'pdbfixer.PDBFixer')
    remove(tmp_pdbfile)
    return tmp_item

def to_molmodmt_MolMod(item, selection=None, syntaxis='mdtraj'):
    from molmodmt.native.io_molmod import from_openmm_Modeller as MolMod_from_openmm_Modeller
    return MolMod_from_openmm_Modeller(item, selection=selection, syntaxis=syntaxis)

def to_pdb(item, filename = None, selection=None, syntaxis='mdtraj'):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    return _openmm_app_PDBFILE.writeFile(item.topology, item.positions, open(filename, 'w'))

def select_with_mdtraj(item, selection):

    tmp_item = to_mdtraj_Topology(item)
    return tmp_item.select(selection)

def duplicate(item):

    from simtk.openmm.app import Modeller as _Modeller

    tmp_item = _Modeller(item.topology, item.positions)
    return tmp_item

def extract_atom_indices(item, atom_indices):

    from molmodmt.utils.atoms_list import complementary_atom_indices
    tmp_item = duplicate(item)
    atoms = list(tmp_item.topology.atoms())
    atoms_to_be_removed = [ atoms[ii] for ii in complementary_atom_indices(item, atom_indices) ]
    tmp_item.delete(atoms_to_be_removed)
    del(atoms, atoms_to_be_removed)
    return tmp_item

def trim_atom_indices(item, atom_indices):

    tmp_item = duplicate(item)
    atoms = list(tmp_item.topology.atoms())
    atoms_to_be_removed = [ atoms[ii] for ii in atom_indices ]
    tmp_item.delete(atoms_to_be_removed)
    del(atoms, atoms_to_be_removed)
    return tmp_item

def merge_two_items(item1, item2):

    from .api_mdtraj_Trajectory import to_openmm_Modeller as _from_mdtraj_Trajectory
    tmp_item1 = to_mdtraj(item1)
    tmp_item2 = to_mdtraj(item2)
    tmp_item = tmp_item1.stack(tmp_item2)
    tmp_item = _from_mdtraj_Trajectory(tmp_item)

    #from molmodmt import duplicate as _duplicate, get as _get
    #tmp_item = duplicate(item1)
    #topology2 = to_openmm_Topology(item2)
    #positions2 = _get(item2, coordinates=True)
    #tmp_item = tmp_item.add(topology2, positions2)

    return tmp_item

###### Set

## atom

def get_n_atoms_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_atoms_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_atom_name_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_name_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_atom_index_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_index_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_atom_id_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_id_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_atom_type_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_type_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_n_residues_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_residues_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_residue_name_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_residue_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_residue_index_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_index_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_residue_id_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_id_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_chain_index_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_index_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_chain_id_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_id_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_n_aminoacids_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_aminoacids_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_n_nucleotides_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_nucleotides_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_n_waters_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_waters_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_n_ions_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_ions_from_atom as _get
    _get(item.topology, indices=indices, frame_indices)

def get_mass_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_mass as _get
    return _get(item, indices)

def get_net_mass_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_net_mass as _get
    return _get(item, indices)

def get_charge_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_charge as _get
    return _get(item, indices)

def get_net_charge_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_net_charge as _get
    return _get(item, indices)

def get_n_degrees_of_freedom_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_degrees_of_freedom_charge as _get
    return _get(item, indices)

def get_molecule_type_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices)

def get_coordinates_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Positions import get_coordinates_from_atom as _get
    return _get(item, indices)

## residue

def get_n_residues_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_residues_from_residue as _get
    return _get(item, indices)

def get_residue_name_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_name_from_residue as _get
    return _get(item, indices)

def get_residue_index_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_index_from_residue as _get
    return _get(item, indices)

def get_residue_id_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_id_from_residue as _get
    return _get(item, indices)

def get_chain_index_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_index_from_residue as _get
    return _get(item, indices)

def get_chain_id_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_id_from_residue as _get
    return _get(item, indices)

def get_molecule_type_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_molecule_type_from_residue as _get
    return _get(item, indices)

## chain

def get_chain_index_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_index_from_chain as _get
    return _get(item, indices)

def get_chain_id_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_id_from_chain as _get
    return _get(item, indices)

def get_n_chains_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_chains_from_chain as _get
    return _get(item, indices)

def get_molecule_type_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_molecule_type_from_chain as _get
    return _get(item, indices)

## system

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_atoms_from_system as _get
    return _get(item, indices)

def get_charge_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get_charge as _get
    return _get(item, indices)

def get_net_charge_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get_net_charge as _get
    return _get(item, indices)

def get_n_degrees_of_freedom_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get_degrees_of_freedom as _get
    return _get(item, indices)




