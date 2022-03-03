_item_fullname_='parmed.GromacsTopologyFile'

def is_parmed_GromacsTopologyFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

