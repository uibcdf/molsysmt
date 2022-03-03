_item_fullname_='openmm.PDBFile'

def is_openmm_PDBFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

