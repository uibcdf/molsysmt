from molmodmt.utils.exceptions import *
from os.path import basename as _basename
from mdtraj.core.topology import Topology as _mdtraj_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

## To other form

def to_aminoacids3_seq(item, selection=None, syntaxis='mdtraj'):

    return ''.join([ r.name for r in item.residues ])

def to_aminoacids1_seq(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as _aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _aminoacids3_to_aminoacids1(tmp_item)
    del(_aminoacids3_to_aminoacids1)
    return tmp_item

def to_openmm_Topology(item, selection=None, syntaxis='mdtraj'):

    return item.to_openmm()

def to_yank_Topography(item, selection=None, syntaxis='mdtraj'):

    from .api_openmm_Topology import to_yank_Topography as _opennn_Topology_to_yank_Topography
    tmp_form = to_openmm_Topology(item)
    tmp_form = _opennn_Topology_to_yank_Topography(tmp_form)
    del(_opennn_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item, selection=None, syntaxis='mdtraj'):

    from .api_openmm_Topology import to_parmed_Structure as _opennn_Topology_to_parmed_Structure
    tmp_form = to_openmm_Topology(item)
    tmp_form = _opennn_Topology_to_parmed_Structure(tmp_form)
    del(_opennn_Topology_to_parmed_Structure)
    return tmp_form

def to_parmed_GromacsTopologyFile(item):
    from parmed.gromacs import GromacsTopologyFile as _GromacsTopologyFile
    tmp_form = to_parmed_Structure(item)
    return _GromacsTopologyFile.from_structure(item)

def to_top(item,filename):
    from .api_parmed_GromacsTopologyFile import to_top as _to_top
    tmp_form = to_parmed_GromacsTopologyFile(item)
    return _to_top(tmp_form,filename)

# Select

def select_with_MDTraj(item, selection):
    return item.select(selection)

# Extract

def extract_atom_indices(item, atoms_selection):
    return item.subset(atoms_selection)

# Merge

def merge_two_items(item1, item2, in_place=False):

    if in_place:
        item1.join(item2)
        pass
    else:
        tmp_item=item1.copy()
        return tmp_item.join(item2)

########################
### Get
########################

## from atom

def get_n_atoms_from_atom (item, indices=None, frame_indices=None):

    return item.n_atoms

def get_n_residues_from_atom (item, indices=None, frame_indices=None):

    return item.n_residues

def get_n_chains_from_atom (item, indices=None, frame_indices=None):

    return item.n_chains

def get_n_molecules_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get
    return len(get(item, indices=indices, molecules=True))

def get_masses_from_atom (item, indices=None, frame_indices=None):

    return [atom.element.mass for atom in item.atoms]

def get_bonded_atoms_from_atom (item, indices=None, frame_indices=None):

    tmp_bonded = [[] for ii in range(item.n_atoms)]
    for bond in item.bonds:
        tmp_bonded[bond.atom1.index].append(bond.atom2.index)
        tmp_bonded[bond.atom2.index].append(bond.atom1.index)
    return tmp_bonded

def get_bonds_from_atom (item, indices=None, frame_indices=None):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.index,bond.atom2.index])
    return tmp_bonds

def get_graph_from_atom (item, indices=None, frame_indices=None):

    return item.to_bondgraph()

def get_molecules_from_atom (item, indices=None, frame_indices=None):

    tmp_molecules = []
    for mm in item.find_molecules():
        tmp_molecules.append([ii.index for ii in mm])
    return tmp_molecules

## from system

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    return item.n_atoms

def get_n_residues_from_system (item, indices=None, frame_indices=None):

    return item.n_residues

def get_n_chains_from_system (item, indices=None, frame_indices=None):

    return item.n_chains

def get_n_bonds_from_system (item, indices=None, frame_indices=None):

    return item.n_bonds

def get_bonded_atoms_from_system (item, indices=None, frame_indices=None):

    tmp_bonded = [[] for ii in range(item.n_atoms)]
    for bond in item.bonds:
        tmp_bonded[bond.atom1.index].append(bond.atom2.index)
        tmp_bonded[bond.atom2.index].append(bond.atom1.index)
    return tmp_bonded

def get_bonds_from_system (item, indices=None, frame_indices=None):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.index,bond.atom2.index])
    return tmp_bonds

def get_graph_from_system (item, indices=None, frame_indices=None):

    return item.to_bondgraph()

def get_molecules_from_system (item, indices=None, frame_indices=None):

    tmp_molecules = []
    for mm in item.find_molecules():
        tmp_molecules.append([ii.index for ii in mm])
    return tmp_molecules

