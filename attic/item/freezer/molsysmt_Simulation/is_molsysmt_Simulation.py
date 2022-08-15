_item_fullname_='molsysmt.Simulation'

def is_molsysmt_Simulation(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

