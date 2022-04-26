_item_fullname_='rdkit.Mol'

def is_rdkit_Mol(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

