
def from_openexplorer_OpenExplorerReporter(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt import box_shape_from_box_vectors
    from molsysmt.native.trajectory import Trajectory
    from numpy import array

    tmp_item = Trajectory()
    tmp_item.step = array(item.step, dtype=int)
    units = item.coordinates.unit
    tmp_item.coordinates = array(item.coordinates._value, dtype=float)
    tmp_item.box = array(item.box._value, dtype=float)
    if atom_indices is not 'all':
        print(tmp_item.coordinates.shape)
        tmp_item.coordinates = tmp_item.coordinates[:,atom_indices,:]
    if frame_indices is not 'all':
        tmp_item.coordinates = tmp_item.coordinates[frame_indices,:,:]
        tmp_item.box = tmp_item.box[frame_indices,:,:]
    tmp_item.coordinates = tmp_item.coordinates*units
    tmp_item.box = tmp_item.box*units

    tmp_item.n_frames = tmp_item.coordinates.shape[0]
    tmp_item.n_atoms = tmp_item.coordinates.shape[1]

    tmp_item.box_shape = box_shape_from_box_vectors(tmp_item.box)

    return tmp_item

