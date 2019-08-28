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
    tmp_item.strip(atom_indices2AmberMask(atom_indices,len(item.atoms),inverse=True))
    return tmp_item

