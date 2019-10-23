from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from parmed.structure import Structure as _parmed_Structure

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_Structure : form_name
}

## Methods

def to_openmm_Modeller(item, atom_indices=None, frame_indices=None):

    from molmodmt import extract as _extract
    from simtk.openmm.app.modeller import Modeller as _openmm_Modeller
    tmp_item = _openm_Modeller(item.topology, item.positions)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices=None, frame_indices=None):

    from mdtraj.core.trajectory import Trajectory as mdtraj_trajectory
    from mdtraj.core.topology import Topology as mdtraj_topology
    from molmodel import extract as _extract

    tmp_item = mdtraj_trajectory(item.positions._value,mdtraj_topology.from_openmm(item.topology))

    if selection is not None:
        tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_nglview(item, atom_indices=None, frame_indices=None):

    from nglview import show_parmed as _nglview_show_parmed
    return _nglview_show_parmed(item)

def to_pdb(item, filename, atom_indices=None, frame_indices=None):

    return item.save(filename)

def to_mol2(item, output_file, atom_indices=None, frame_indices=None):

    return item.save(filename)

def select_with_MDTraj(item, selection):
    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def select_with_ParmEd(item, selection):
    from parmed.amber import AmberMask as _AmberMask
    tmp_sel = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)
    return tmp_sel

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    mode='keeping_selection'

    from molmodmt.utils.atom_indices import atom_indices_to_AmberMask
    from molmodmt.utils.atom_indices import complementary_atom_indices
    if mode=='removing_selection':
        mask = atom_indices_to_AmberMask(item, atom_indices)
    elif mode=='keeping_selection':
        tmp_atom_indices = complementary_atom_indices(item, atom_indices)
        mask = atom_indices_to_AmberMask(item, tmp_atom_indices)
    from copy import deepcopy
    tmp_item = deepcopy(item)
    tmp_item.strip(atom_indices2AmberMask(atom_indices,len(item.atoms),inverse=True))
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


## system

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    return len(item.atoms)

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

