
def is_mdtraj_DCDTrajectoryFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return item_fullname == 'mdtraj.formats.dcd.DCDTrajectoryFile'

