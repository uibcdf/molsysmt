_item_fullname_='openmm.GromacsTopFile'

def is_openmm_GromacsTopFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

