from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory import Trajectory as _molmodmt_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Trajectory : form_name,
    'molmodmt.Trajectory' : form_name
}

def getting(item, atom_indices=None, **kwargs):

    from .api_mdtraj_Topology import getting as _get

    if atom_indices is not None:
        from .api_mdtraj_Topology import extract_atom_indices as _mdtraj_extract
        tmp_topology = _mdtraj_extract(item.topology_mdtraj,atom_indices)
    else:
        tmp_topology = item.topology_mdtraj

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_topology.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            result.append(item.n_frames)
        if option=='n_residues' and kwargs[option]==True:
            result.append(_get(tmp_topology,n_residues=True))
        if option=='n_molecules' and kwargs[option]==True:
            result.append(_get(tmp_topology,n_molecules=True))
        if option=='masses' and kwargs[option]==True:
            result.append(_get(tmp_topology,masses=True))
        if option=='bonded_atoms' and kwargs[option]==True:
            result.append(_get(tmp_topology,bonded_atoms=True))
        if option=='bonds' and kwargs[option]==True:
            result.append(_get(tmp_topology,bonds=True))
        if option=='graph' and kwargs[option]==True:
            result.append(_get(tmp_topology,graph=True))
        if option=='molecules' and kwargs[option]==True:
            result.append(_get(tmp_topology,molecules=True))
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError

    if len(result)==1:
        return result[0]
    else:
        return result

def select_with_mdtraj(item, selection):
    from .api_mdtraj_Topology import select_with_mdtraj as _select_with_mdtraj
    return _select_with_mdtraj(item.topology_mdtraj,selection)

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


