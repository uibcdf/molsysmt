
def is_openmm_Modeller(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_=='openmm.Modeller'

