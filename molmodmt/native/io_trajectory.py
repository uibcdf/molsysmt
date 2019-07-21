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
#
#def from_pdb(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from molmodmt import convert as _convert
#    tmp_item = _convert(item, form='mdtraj.Trajectory', selection=selection, syntaxis=syntaxis)
#    tmp_item = from_mdtraj_Trajectory(tmp_item)
#    return tmp_item
#
#def from_xtc(item=None, topology=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from molmodmt import extract as _extract
#    tmp_item = _Trajectory(filename=item, topology=topology)
#    if frame_indices is not None:
#        tmp_item.load(frame_indices=frame_indices, selection=selection, syntaxis=syntaxis)
#    return tmp_item

def from_hdf5(item=None, atom_indices='all', frame_indices='all'):

    from .trajectory import Trajectory
    tmp_item = Trajectory(filename=item)
    if frame_indices is not None:
        tmp_item.load(frame_indices=frame_indices, atom_indices=atom_indices)
    return tmp_item

