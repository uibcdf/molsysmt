
def is_pytraj_Trajectory(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'pytraj.Trajectory')

    return output

