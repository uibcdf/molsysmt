from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from parmed.structure import Structure as _parmed_Structure

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_Structure : form_name
}

def to_mdtraj(item):

    from mdtraj.core.trajectory import Trajectory as mdtraj_trajectory
    from mdtraj.core.topology import Topology as mdtraj_topology

    return mdtraj_trajectory(item.positions._value,mdtraj_topology.from_openmm(item.topology))

def to_nglview(item):

    from nglview import show_parmed as _nglview_show_parmed
    return _nglview_show_parmed(item)

def to_pdb(item,output_file):

    return item.save(output_file)

def to_mol2(item,output_file):

    return item.save(output_file)

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

def extract_atoms_list(item, atoms_list):
    from molmodmt.utils.miscellanea import atoms_list2AmberMask
    from copy import deepcopy
    tmp_item = deepcopy(item)
    tmp_item.strip(atoms_list2AmberMask(atoms_list,len(item.atoms),inverse=True))
    return tmp_item

def get(item, atoms_list=None, **kwargs):

    if atoms_list is not None:
        tmp_topology = extract_atoms_list(item,atoms_list)
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
            for bond in st.bonds:
                tmp_bonds.append([bond.atom1.idx,bond.atom2.idx])
            result.append(tmp_bonds)
        if option=='graph' and kwargs[options]==True:
            from networks import Graph as _Graph
            result.append(get(item,bonds=True))
        if option=='molecules' and kwargs[option]==True:
            from networks import connected_components as _connected_componentes
            tmp_graph = get(item, graph=True)
            result.append([list(ii) for ii in networkx.connected_components(g)])

    if len(result)==1:
        return result[0]
    else:
        return result

