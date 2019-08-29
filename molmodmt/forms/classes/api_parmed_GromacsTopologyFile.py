from os.path import basename as _basename
from parmed.gromacs.gromacstop import GromacsTopologyFile as _parmed_GromacsTopologyFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_GromacsTopologyFile : form_name
}

def to_mdtraj_Topology(item, selection=None, syntaxis='MDTraj'):

    from mdtraj.core.topology import Topology as mdtraj_topology
    return mdtraj_topology.from_openmm(item.topology)

def to_mol2(item, filename, selection=None, syntaxis='MDTraj'):
    return item.save(filename)

def to_top(item, filename, selection=None, syntaxis='MDTraj'):
    return item.save(filename)

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

def extract_atom_indices(item, atom_indices):

    return trim_atom_indices(item, atom_indices, mode='keeping_selection')

def trim_atom_indices(item, atom_indices, mode='removing_selection'):

    from molmodmt.utils.atom_indices import atom_indices_to_AmberMask
    from molmodmt.utils.atom_indices import complementary_atom_indices
    if mode=='removing_selection':
        mask = atom_indices_to_AmberMask(item, atom_indices)
    elif mode=='keeping_selection':
        tmp_atom_indices = complementary_atom_indices(item, atom_indices)
        mask = atom_indices_to_AmberMask(item, tmp_atom_indices)
    from copy import deepcopy
    tmp_item = deepcopy(item)
    tmp_item.strip(atom_indices_to_AmberMask(tmp_item,atom_indices))
    return tmp_item

##### Set

## Atom

def get_n_atoms_from_atom (item, indices=None, frame_indices=None):

    return len(item.atoms)

def get_n_residues_from_atom (item, indices=None, frame_indices=None):

    return len(item.residues)

def get_mass_from_atom (item, indices=None, frame_indices=None):

    return [atom.mass for atom in item.atoms]

def get_bonded_atoms_from_atom (item, indices=None, frame_indices=None):

    tmp_bonded = [[] for ii in range(len(st.atoms))]
    for bond in st.bonds:
        tmp_bonded[bond.atom1.idx].append(bond.atom2.idx)
        tmp_bonded[bond.atom2.idx].append(bond.atom1.idx)

    return tmp_bonded

def get_bonds_from_atom (item, indices=None, frame_indices=None):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.idx,bond.atom2.idx])

    return tmp_bonds

def get_graph_from_atom (item, indices=None, frame_indices=None):

    from networkx import Graph as _Graph
    tmp_graph = _Graph(getting(item,bonds=True))
    for atom in item.atoms:
        if len(atom.bonds)==0:
            tmp_graph.add_node(atom.idx)
    result.append(tmp_graph)

def get_molecules_from_atom (item, indices=None, frame_indices=None):

    from networkx import connected_components as _connected_components
    tmp_graph = getting(item, graph=True)
    result.append([list(ii) for ii in _connected_components(tmp_graph)])

def get_molecule_type_from_atom (item, indices=None, frame_indices=None):

    from molmodmt.utils.types import residue2molecule_types
    tmp_molecules = getting(item,molecules=True)
    tmp_types = []
    for molecule in tmp_molecules:
        tmp_types.append(residue2molecule_types(item.atoms[molecule[0]].residue.name))
    if len(tmp_types)==1:
        tmp_types=tmp_types[0]
    return tmp_types

## System

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    return len(item.atoms)


