_item_fullname_='pytraj.Trajectory'

def is_pytraj_Trajectory(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

