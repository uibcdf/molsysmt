_item_fullname_='mdtraj.Topology'

def is_mdtraj_Topology(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

