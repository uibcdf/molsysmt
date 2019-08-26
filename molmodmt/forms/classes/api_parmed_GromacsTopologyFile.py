from os.path import basename as _basename
from parmed.gromacs.gromacstop import GromacsTopologyFile as _parmed_GromacsTopologyFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_GromacsTopologyFile : form_name
}

def to_mdtraj_Topology(item):

    from mdtraj.core.topology import Topology as mdtraj_topology
    return mdtraj_topology.from_openmm(item.topology)

def to_mol2(item,filename):
    return item.save(filename)

def to_top(item,filename):
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
    from molmodmt.utils.miscellanea import atom_indices2AmberMask
    from copy import deepcopy
    tmp_item = deepcopy(item)
    tmp_item.strip(atom_indices2AmberMask(atom_indices,len(item.atoms),inverse=True))
    return tmp_item

