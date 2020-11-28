from os.path import basename as _basename
from parmed.gromacs.gromacstop import GromacsTopologyFile as _parmed_GromacsTopologyFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_GromacsTopologyFile : form_name
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_parameters=False

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology as mdtraj_topology
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_topology.from_openmm(tmp_item)
    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import extract as extract_openmm_topology
    tmp_item = item.topology
    tmp_item = extract_openmm_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mol2(item, output_filepath=None, atom_indices='all', frame_indices='all'):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return item.save(output_filepath)

def to_top(item, output_filepath=None, atom_indices='all', frame_indices='all'):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return item.save(output_filepath)

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj_Topology(item)
    tmp_sel=tmp_form.select(selection)
    del(tmp_form)
    return tmp_sel

def select_with_ParmEd(item, selection):

    from parmed.amber import AmberMask as _AmberMask
    tmp_sel = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)
    return tmp_sel

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from copy import deepcopy
        from molsysmt.utils.atom_indices import atom_indices_to_AmberMask
        from molsysmt.utils.atom_indices import complementary_atom_indices
        tmp_atom_indices = complementary_atom_indices(item, atom_indices)
        mask = atom_indices_to_AmberMask(item, tmp_atom_indices)
        tmp_item = copy(item)
        tmp_item.strip(atom_indices_to_AmberMask(tmp_item,atom_indices))
        return tmp_item

def copy(item):

    from copy import deepcopy
    return deepcopy(item)

##### Set

## Atom

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    return len(item.atoms)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    return len(item.groups)

def get_mass_from_atom (item, indices='all', frame_indices='all'):

    return [atom.mass for atom in item.atoms]

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    tmp_bonded = [[] for ii in range(len(st.atoms))]
    for bond in st.bonds:
        tmp_bonded[bond.atom1.idx].append(bond.atom2.idx)
        tmp_bonded[bond.atom2.idx].append(bond.atom1.idx)

    return tmp_bonded

def get_bonds_from_atom (item, indices='all', frame_indices='all'):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.idx,bond.atom2.idx])

    return tmp_bonds

def get_graph_from_atom (item, indices='all', frame_indices='all'):

    from networkx import Graph as _Graph
    tmp_graph = _Graph(getting(item,bonds=True))
    for atom in item.atoms:
        if len(atom.bonds)==0:
            tmp_graph.add_node(atom.idx)
    result.append(tmp_graph)

def get_molecules_from_atom (item, indices='all', frame_indices='all'):

    from networkx import connected_components as _connected_components
    tmp_graph = getting(item, graph=True)
    result.append([list(ii) for ii in _connected_components(tmp_graph)])

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.utils.types import group2molecule_types
    tmp_molecules = getting(item,molecules=True)
    tmp_types = []
    for molecule in tmp_molecules:
        tmp_types.append(group2molecule_types(item.atoms[molecule[0]].group.name))
    if len(tmp_types)==1:
        tmp_types=tmp_types[0]
    return tmp_types

## System

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return len(item.atoms)

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

