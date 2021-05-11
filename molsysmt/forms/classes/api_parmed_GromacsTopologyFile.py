from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from parmed.gromacs.gromacstop import GromacsTopologyFile as _parmed_GromacsTopologyFile
from molsysmt.molecular_system import molecular_system_components

form_name='parmed.GromacsTopologyFile'

is_form={
    _parmed_GromacsTopologyFile : form_name
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds']:
    has[ii]=True

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology as mdtraj_topology

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_topology.from_openmm(tmp_item)
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = opennmm_Topology_to_openmm_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mol2(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    tmp_item, tmp_molecular_system = to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    item.save(output_filename)
    tmp_item = output_filename
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_top(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    tmp_item, tmp_molecular_system = to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    item.save(output_filename)
    tmp_item = output_filename
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

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

def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', frame_indices='all', copy_if_all=True):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):

        from copy import deepcopy
        tmp_item = deepcopy(item)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    else:

        from copy import deepcopy
        from molsysmt._private_tools.atom_indices import atom_indices_to_AmberMask
        from molsysmt._private_tools.atom_indices import complementary_atom_indices
        tmp_atom_indices = complementary_atom_indices(item, atom_indices)
        mask = atom_indices_to_AmberMask(item, tmp_atom_indices)
        tmp_item = copy(item)
        tmp_item.strip(atom_indices_to_AmberMask(tmp_item,atom_indices))
        tmp_molecular_system = molecular_system.combine_with_items(item)

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

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

    from molsysmt._private_tools.types import group2molecule_types
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

    return None


