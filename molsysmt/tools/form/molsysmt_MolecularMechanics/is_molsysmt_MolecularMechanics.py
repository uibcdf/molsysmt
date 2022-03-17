_item_fullname_='molsysmt.MolecularMechanics'

def is_molsysmt_MolecularMechanics(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

