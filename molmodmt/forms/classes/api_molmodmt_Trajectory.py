from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory import Trajectory as _molmodmt_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Trajectory : form_name,
    'molmodmt.Trajectory' : form_name
}

# Methods

def select_with_MDTraj(item, selection):
    from .api_mdtraj_Topology import select_with_MDTraj as _select_with_MDTraj
    return _select_with_MDTraj(item.topology_mdtraj,selection)

def extract_atom_indices(item, atom_indices):
    return item.extract(atom_indices)

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):
    from molmodmt.native.io_trajectory import to_mdtraj_Trajectory as _to_mdtraj_Trajectory
    return _to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):
    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_parmed_GromacsTopologyFile(item, selection=None, syntaxis='mdtraj'):
    from .api_mdtraj_Topology import to_parmed_GromacsTopologyFile as _to_GromacsTopologyFile
    return _to_GromacsTopologyFile(item.topology_mdtraj, selection=selection, syntaxis=syntaxis)

def to_xtc(item,filename=None, selection=None, syntaxis='mdtraj'):
    from .api_mdtraj_Trajectory import to_xtc as _to_xtc
    tmp_item=to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)
    return _to_xtc(tmp_item,filename)

def to_top(item,filename=None, selection=None, syntaxis='mdtraj'):
    from .api_mdtraj_Topology import to_top as _to_top
    return _to_top(item.topology_mdtraj,filename, selection=selection, syntaxis=syntaxis)

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview

    if type(item) in [list,tuple]:
        tmp_item = []
        for ii in item:
            tmp_item.append(to_mdtraj_Trajectory(ii))
    else:
        tmp_item = to_mdtraj_Trajectory(item)

    return _mdtraj_to_nglview(tmp_item)

###### Set

## atom

## residue

## chain

## system


