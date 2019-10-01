import numpy as _np

#def parse_mdtraj_Trajectory(item=None, atom_indices='all', frame_indices='all'):
#
#    tmp_xyz = item.xyz
#
#    if selection is not None:
#        from molmodmt import select as _select
#        list_atoms = _select(item, selection=selection, syntaxis='MDTraj')
#        tmp_xyz = tmp_xyz[:,list_atoms,:]
#
#    if frame_indices is not None:
#        tmp_xyz = tmp_xyz[frame_indices,:,:]
#
#    tmp_coordinates = _np.asfortranarray(tmp_xyz) # the same array and same units
#    tmp_box = _np.asfortranarray(item.unitcell_vectors)
#    tmp_time = _np.asfortranarray(item.time)
#    try:
#        tmp_timestep = item.timestep
#    except:
#        tmp_timestep = None
#
#    del(tmp_xyz)
#    return tmp_coordinates, tmp_box, tmp_time, tmp_timestep
#
#def from_mdtraj(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    return from_mdtraj_Trajectory(item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)
#
#def from_mdtraj_Trajectory(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    tmp_item = _Trajectory()
#    tmp_item._import_mdtraj_data(item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)
#    return tmp_item
#
#def from_openmm_Modeller(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from molmodmt import convert as _convert
#    tmp_item = _Trajectory()
#    tmp_mdtraj_item = _convert(item, 'mdtraj.Trajectory')
#    tmp_item.parse_mdtraj_Trajectory(tmp_mdtraj_item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)
#    del(tmp_mdtraj_item)
#    return tmp_item


def from_pdb(item=None, atom_indices=None, frame_indices=None):

    from .trajectory import Trajectory
    tmp_item = Trajectory(filename=item)
    tmp_item.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def from_xtc(item=None, atom_indices=None, frame_indices=None):

    from .trajectory import Trajectory
    tmp_item = Trajectory(filename=item)
    tmp_item.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def from_hdf5(item=None, atom_indices=None, frame_indices=None):

    from .trajectory import Trajectory
    tmp_item = Trajectory(filename=item)
    tmp_item.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

