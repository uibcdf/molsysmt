from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from parmed.structure import Structure as _parmed_Structure

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_Structure : form_name
}

def to_openmm_Modeller(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from simtk.openmm.app.modeller import Modeller as _openmm_Modeller
    tmp_item = _openm_Modeller(item.topology, item.positions)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from mdtraj.core.trajectory import Trajectory as mdtraj_trajectory
    from mdtraj.core.topology import Topology as mdtraj_topology
    from molmodel import extract as _extract

    tmp_item = mdtraj_trajectory(item.positions._value,mdtraj_topology.from_openmm(item.topology))

    if selection is not None:
        tmp_item = _extract(tmp_item, selection=selection, syntaxis='mdtraj')

    return tmp_item

def to_nglview(item):

    from nglview import show_parmed as _nglview_show_parmed
    return _nglview_show_parmed(item)

def to_pdb(item, filename):

    return item.save(filename)

def to_mol2(item,output_file):

    return item.save(filename)

def select_with_mdtraj(item, selection):
    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def select_with_parmed(item, selection):
    from parmed.amber import AmberMask as _AmberMask
    tmp_sel = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)
    return tmp_sel

def extract_atom_indices(item, atom_indices):
    from molmodmt.utils.miscellanea import atom_indices2AmberMask
    from copy import deepcopy
    tmp_item = deepcopy(item)
    tmp_item.strip(atom_indices2AmberMask(atom_indices,len(item.atoms),inverse=True))
    return tmp_item

def get(item, atom_indices=None, **kwargs):

    if atom_indices is not None:
        tmp_topology = extract_atom_indices(item,atom_indices)
    else:
        tmp_topology = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(len(item.atoms))
        if option=='n_frames' and kwargs[option]==True:
            raise BadCallError
        if option=='n_residues' and kwargs[option]==True:
            result.append(len(item.residues))
        if option=='n_molecules' and kwargs[option]==True:
            raise BadCallError
        if option=='masses' and kwargs[option]==True:
            tmp_masses=[atom.mass for atom in item.atoms]
            result.append(tmp_masses)
        if option=='bonded_atoms' and kwargs[option]==True:
            tmp_bonded = [[] for ii in range(len(st.atoms))]
            for bond in st.bonds:
                tmp_bonded[bond.atom1.idx].append(bond.atom2.idx)
                tmp_bonded[bond.atom2.idx].append(bond.atom1.idx)
            result.append(tmp_bonded)
        if option=='bonds' and kwargs[option]==True:
            tmp_bonds = []
            for bond in item.bonds:
                tmp_bonds.append([bond.atom1.idx,bond.atom2.idx])
            result.append(tmp_bonds)
        if option=='graph' and kwargs[option]==True:
            from networkx import Graph as _Graph
            tmp_graph = _Graph(get(item,bonds=True))
            for atom in item.atoms:
                if len(atom.bonds)==0:
                    tmp_graph.add_node(atom.idx)
            result.append(tmp_graph)
        if option=='molecules' and kwargs[option]==True:
            from networkx import connected_components as _connected_components
            tmp_graph = get(item, graph=True)
            result.append([list(ii) for ii in _connected_components(tmp_graph)])
        if option=='molecule_type' and kwargs[option]==True:
            from molmodmt.utils.types import residue2molecule_types
            tmp_molecules = get(item,molecules=True)
            tmp_types = []
            for molecule in tmp_molecules:
                tmp_types.append(residue2molecule_types(item.atoms[molecule[0]].residue.name))
            if len(tmp_types)==1:
                tmp_types=tmp_types[0]
            result.append(tmp_types)
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError

    if len(result)==1:
        return result[0]
    else:
        return result

