from molmodmt.utils.exceptions import *
from os.path import basename as _basename
from mdtraj.core.topology import Topology as _mdtraj_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

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

def select_with_mdtraj(item, selection):
    return item.select(selection)

def extract_atom_indices(item, atoms_selection):
    return item.subset(atoms_selection)

def merge_two_items(item1, item2, in_place=False):

    if in_place:
        item1.join(item2)
        pass
    else:
        tmp_item=item1.copy()
        return tmp_item.join(item2)

def get(item, atom_indices=None, **kwargs):

    if atom_indices is not None:
        tmp_item = extract_atom_indices(item,atom_indices)
    else:
        tmp_item = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_item.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            raise BadCallError(BadCallMessage)
        if option=='n_residues' and kwargs[option]==True:
            result.append(tmp_item.n_residues)
        if option=='n_chains' and kwargs[option]==True:
            result.append(tmp_item.n_chains)
        if option=='n_molecules' and kwargs[option]==True:
            result.append(len(get(tmp_item,molecules=True)))
        if option=='masses' and kwargs[option]==True:
            result.append([atom.element.mass for atom in tmp_item.atoms])
        if option=='bonded_atoms' and kwargs[option]==True:
            tmp_bonded = [[] for ii in range(item.n_atoms)]
            for bond in item.bonds:
                tmp_bonded[bond.atom1.index].append(bond.atom2.index)
                tmp_bonded[bond.atom2.index].append(bond.atom1.index)
            result.append(tmp_bonded)
        if option=='bonds' and kwargs[option]==True:
            tmp_bonds = []
            for bond in item.bonds:
                tmp_bonds.append([bond.atom1.index,bond.atom2.index])
            result.append(tmp_bonds)
        if option=='graph' and kwargs[option]==True:
            result.append(item.to_bondgraph())
        if option=='chain_name' and kwargs[option] is not None:
            raise NotImplementedError
        if option=='chain_names' and kwargs[option] is not None:
            raise NotImplementedError
        if option=='molecules' and kwargs[option]==True:
            tmp_molecules = []
            for mm in item.find_molecules():
                tmp_molecules.append([ii.index for ii in mm])
            result.append(tmp_molecules)
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError

    del(tmp_item)

    if len(result)==1:
        return result[0]
    else:
        return result



