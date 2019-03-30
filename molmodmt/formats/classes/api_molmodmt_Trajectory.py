from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory import Trajectory as _molmodmt_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Trajectory : form_name
}

def get_info(item, atoms_list=None, **kwargs):

    from .api_mdtraj_Topology import get_info as _get_info

    if atoms_list is not None:
        from .api_mdtraj_Topology import extract_atoms_list as _mdtraj_extract
        tmp_topology = _mdtraj_extract(item.topology_mdtraj,atoms_list)
    else:
        tmp_topology = item.topology_mdtraj

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_topology.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            result.append(item.n_frames)
        if option=='n_residues' and kwargs[option]==True:
            result.append(_get_item(tmp_topology,n_residues=True))
        if option=='n_molecules' and kwargs[option]==True:
            result.append(_get_info(tmp_topology,n_molecules=True))
        if option=='masses' and kwargs[option]==True:
            result.append(_get_info(tmp_topology,masses=True))

    if len(result)==1:
        return result[0]
    else:
        return result

def select_with_mdtraj(item, selection):
    from .api_mdtraj_Topology import select_with_mdtraj as _select_with_mdtraj
    return _select_with_mdtraj(item.topology_mdtraj,selection)

def extract_atoms_list(item, atoms_list):
    return item.extract(atoms_list)

def to_mdtraj_Trajectory(item):
    from molmodmt.native.io_trajectory import to_mdtraj_Trajectory as _to_mdtraj_Trajectory
    return _to_mdtraj_Trajectory(item)

def to_mdtraj(item):
    return to_mdtraj_Trajectory(item)

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview

    if type(item) in [list,tuple]:
        tmp_item = []
        for ii in item:
            tmp_item.append(to_mdtraj_Trajectory(ii))
    else:
        tmp_item = to_mdtraj_Trajectory(item)

    return _mdtraj_to_nglview(tmp_item)

def get_molecules(item,with_bonds):
    from .api_mdtraj_Trajectory import get_molecules as _get_molecules
    return _get_molecules(item.topology_mdtraj,with_bonds)


