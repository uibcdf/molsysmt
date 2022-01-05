_item_fullname_='openff.toolkit.topology.Topology'

def is_openff_Topology(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

