_item_fullname_='mdtraj.Trajectory'

def is_mdtraj_Trajectory(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

