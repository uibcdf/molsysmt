from os.path import basename as _basename
from mdtraj.core.topology import Topology as _mdtraj_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

def to_openmm_Topology(item):

    return item.to_openmm()

def to_yank_Topography(item):

    from .api_openmm_Topology import to_yank_Topography as _opennn_Topology_to_yank_Topography
    tmp_form = to_openmm_Topology(item)
    tmp_form = _opennn_Topology_to_yank_Topography(tmp_form)
    del(_opennn_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item):

    from .api_openmm_Topology import to_parmed_Structure as _opennn_Topology_to_parmed_Structure
    tmp_form = to_openmm_Topology(item)
    tmp_form = _opennn_Topology_to_parmed_Structure(tmp_form)
    del(_opennn_Topology_to_parmed_Structure)
    return tmp_form

def select_with_mdtraj(item, selection):
    return item.select(selection)

def extract_atoms_list(item, atoms_selection):
    return item.subset(atoms_selection)

def merge_two_items(item1, item2, in_place=False):

    if in_place:
        item1.join(item2)
        pass
    else:
        tmp_item=item1.copy()
        return tmp_item.join(item2)

def get_molecules(item,with_bonds=False):

    tmp_molecules = []
    for mm in item.find_molecules():
        tmp_molecules.append([ii.index for ii in mm])
    if with_bonds:
        tmp_bonds = [[] for ii in range(item.n_atoms)]
        for bond in item.bonds:
            tmp_bonds[bond.atom1.index].append(bond.atom2.index)
            tmp_bonds[bond.atom2.index].append(bond.atom1.index)
        return tmp_molecules,tmp_bonds
    else:
        return tmp_molecules


        #for bb in item.subset(tmp_list_atoms).bonds:
        #    tmp_bonds.append([bb.atom1.index,bb.atom2.index])
        #tmp_molecules.append([_np.array(tmp_list_atoms),_np.array(tmp_bonds)])
    #del(molecule_sets,tmp_list_atoms,tmp_bonds)
    #return tmp_molecules


