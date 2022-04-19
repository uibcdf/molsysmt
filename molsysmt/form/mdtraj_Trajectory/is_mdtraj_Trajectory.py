def is_mdtraj_Trajectory(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdtraj.core.trajectory.Trajectory')

    return output

