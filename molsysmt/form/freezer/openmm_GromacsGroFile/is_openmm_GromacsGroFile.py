_item_fullname_='openmm.GromacsGroFile'

def is_openmm_GromacsGroFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

